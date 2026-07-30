import pytest
from tahmures.context import ContextBudgetError, ContextItem, select_context
from tahmures.contracts import FieldContract, OutputContract
from tahmures.templates import PromptTemplate, TemplateField, TemplateValidationError
from tahmures.workflow import WorkflowPlan, WorkflowStep, WorkflowValidationError


def test_prompt_template_rejects_bad_inputs_and_does_not_dispatch() -> None:
    template = PromptTemplate(
        "decree-v1",
        "Send ${allowance} to ${province}",
        (TemplateField("allowance", int), TemplateField("province", str)),
    )
    rendered = template.render({"allowance": 12, "province": "Ray"})
    assert rendered.text == "Send 12 to Ray"
    with pytest.raises(TemplateValidationError):
        template.render({"allowance": "12", "province": "Ray"})
    with pytest.raises(TemplateValidationError):
        template.render({"allowance": 12, "province": "${other}"})


def test_output_contract_rejects_syntax_type_enum_and_extra_fields() -> None:
    contract = OutputContract(
        (
            FieldContract("id", "string"),
            FieldContract("status", "string", allowed_values=("current", "expired")),
            FieldContract("count", "integer"),
        )
    )
    assert contract.validate('{"id":"T-1","status":"current","count":2}').valid
    assert not contract.validate("not-json").parsed
    assert not contract.validate('{"id":"T-1","status":"unknown","count":2}').valid
    assert not contract.validate(
        '{"id":"T-1","status":"current","count":true,"extra":1}'
    ).valid


def test_workflow_detects_cycles_and_calculates_ready_steps() -> None:
    locate = WorkflowStep("locate", inputs=("mission",), outputs=("position",))
    assess = WorkflowStep(
        "assess",
        depends_on=("locate",),
        inputs=("position",),
        outputs=("condition",),
        checkpoint=True,
    )
    report = WorkflowStep(
        "report",
        depends_on=("assess",),
        inputs=("condition",),
        outputs=("record",),
        terminal=True,
    )
    plan = WorkflowPlan((locate, assess, report))
    plan.validate()
    assert [step.id for step in plan.ready({"locate"})] == ["assess"]
    cyclic = WorkflowPlan(
        (
            WorkflowStep("a", ("b",), ("input",), ("a-out",), checkpoint=True),
            WorkflowStep("b", ("a",), ("a-out",), ("b-out",), terminal=True),
        )
    )
    with pytest.raises(WorkflowValidationError):
        cyclic.validate()


def test_context_selection_preserves_mandatory_provenance_and_reports_exclusions() -> (
    None
):
    items = (
        ContextItem("task", "current task", 2, 10, "application", mandatory=True),
        ContextItem("low", "old note", 3, 1, "archive:L"),
        ContextItem("high", "decisive note", 3, 9, "archive:H"),
    )
    selected = select_context(items, 5)
    assert [item.id for item in selected.selected] == ["task", "high"]
    assert [item.id for item in selected.excluded] == ["low"]
    assert selected.selected[1].provenance == "archive:H"
    with pytest.raises(ContextBudgetError):
        select_context(items, 1)
