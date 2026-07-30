package tahmures

import (
	"context"
	"fmt"
)

type Client interface {
	Name() string
	Generate(context.Context, GenerationRequest) (GenerationResponse, error)
}

type FixtureClient struct {
	fixtures map[string]GenerationResponse
}

func NewFixtureClient(records []FixtureRecord) *FixtureClient {
	fixtures := make(map[string]GenerationResponse, len(records))
	for _, record := range records {
		fixtures[fixtureKey(record.CaseID, record.VariantID, record.Trial)] = record.Response
	}
	return &FixtureClient{fixtures: fixtures}
}

func (client *FixtureClient) Name() string {
	return "fixture"
}

func (client *FixtureClient) Generate(
	_ context.Context,
	request GenerationRequest,
) (GenerationResponse, error) {
	caseID, caseOK := request.Metadata["case_id"].(string)
	variantID, variantOK := request.Metadata["variant_id"].(string)
	trialFloat, trialOK := request.Metadata["trial"].(int)
	if !trialOK {
		if value, ok := request.Metadata["trial"].(float64); ok {
			trialFloat, trialOK = int(value), true
		}
	}
	if !caseOK || !variantOK || !trialOK {
		return GenerationResponse{}, fmt.Errorf(
			"fixture requests require case_id, variant_id, trial",
		)
	}
	response, ok := client.fixtures[fixtureKey(caseID, variantID, trialFloat)]
	if !ok {
		return GenerationResponse{}, fmt.Errorf(
			"no fixture response for %s/%s/%d",
			caseID,
			variantID,
			trialFloat,
		)
	}
	return response, nil
}

func fixtureKey(caseID, variantID string, trial int) string {
	return fmt.Sprintf("%s|%s|%d", caseID, variantID, trial)
}
