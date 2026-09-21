package tahmures

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
)

type CapabilityRequest struct {
	RequestID, Principal, Action string
	Arguments                    map[string]any
	Scopes                       []string
	Effect                       string
	ExpiresAt                    int
}
type ApprovalRecord struct {
	RequestID, RequestDigest, Approver string
	Approved                           bool
	At                                 int
}
type ApprovalPolicy struct {
	AllowedActions                       []string
	PrincipalScopes                      map[string][]string
	ApprovalEffects, DualApprovalEffects []string
}
type AuthorizationResult struct {
	Allowed       bool
	Reason        string
	ApprovalCount int
	Audit         map[string]string
}

func RequestDigest(action string, arguments map[string]any) string {
	encoded, _ := json.Marshal(map[string]any{"action": action, "arguments": arguments})
	sum := sha256.Sum256(encoded)
	return hex.EncodeToString(sum[:])
}
func Authorize(request CapabilityRequest, approvals []ApprovalRecord, policy ApprovalPolicy, now int) AuthorizationResult {
	digest := RequestDigest(request.Action, request.Arguments)
	audit := map[string]string{"request_id": request.RequestID, "principal": request.Principal, "action": request.Action, "digest": digest}
	reject := func(reason string, count int) AuthorizationResult {
		return AuthorizationResult{false, reason, count, audit}
	}
	if request.RequestID == "" || request.Principal == "" || request.Action == "" {
		return reject("invalid_request", 0)
	}
	if !stringSetAny([]string{"read", "write", "high_consequence"})[request.Effect] {
		return reject("invalid_effect", 0)
	}
	if now >= request.ExpiresAt {
		return reject("request_expired", 0)
	}
	if !stringSetAny(policy.AllowedActions)[request.Action] {
		return reject("unknown_action", 0)
	}
	granted := stringSetAny(policy.PrincipalScopes[request.Principal])
	for _, scope := range request.Scopes {
		if !granted[scope] {
			return reject("insufficient_scope", 0)
		}
	}
	approvers := map[string]bool{}
	for _, approval := range approvals {
		if approval.RequestID != request.RequestID {
			continue
		}
		if approval.RequestDigest != digest {
			return reject("digest_mismatch", 0)
		}
		if approval.Approved && approval.At <= now {
			if approvers[approval.Approver] {
				return reject("duplicate_approver", len(approvers))
			}
			approvers[approval.Approver] = true
		}
	}
	approvalEffects := policy.ApprovalEffects
	if approvalEffects == nil {
		approvalEffects = []string{"write"}
	}
	required := 0
	if stringSetAny(policy.DualApprovalEffects)[request.Effect] {
		required = 2
	} else if stringSetAny(approvalEffects)[request.Effect] {
		required = 1
	}
	if len(approvers) < required {
		return reject("approval_required", len(approvers))
	}
	return AuthorizationResult{true, "allowed", len(approvers), audit}
}
