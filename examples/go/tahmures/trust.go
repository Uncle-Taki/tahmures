package tahmures

import "fmt"

type ContentRecord struct{ RecordID, Text, Source, DeclaredRole, Provenance string }
type TrustPolicy struct{ TrustedInstructionSources, RejectedSources []string }
type TrustFinding struct{ RecordID, Reason string }
type TrustPartition struct {
	Instructions, Data, Rejected []ContentRecord
	Findings                     []TrustFinding
}

func PartitionContent(records []ContentRecord, policy TrustPolicy) (TrustPartition, error) {
	seen := map[string]bool{}
	trusted, rejectedSources := stringSetAny(policy.TrustedInstructionSources), stringSetAny(policy.RejectedSources)
	result := TrustPartition{}
	for _, record := range records {
		if record.RecordID == "" || record.Text == "" || record.Source == "" || record.Provenance == "" || seen[record.RecordID] {
			return TrustPartition{}, fmt.Errorf("invalid or duplicate content record")
		}
		seen[record.RecordID] = true
		if record.DeclaredRole != "instruction" && record.DeclaredRole != "data" {
			return TrustPartition{}, fmt.Errorf("content role must be instruction or data")
		}
		if rejectedSources[record.Source] {
			result.Rejected = append(result.Rejected, record)
			result.Findings = append(result.Findings, TrustFinding{record.RecordID, "source_rejected"})
		} else if record.DeclaredRole == "instruction" && trusted[record.Source] {
			result.Instructions = append(result.Instructions, record)
		} else {
			result.Data = append(result.Data, record)
			if record.DeclaredRole == "instruction" {
				result.Findings = append(result.Findings, TrustFinding{record.RecordID, "authority_downgraded"})
			}
		}
	}
	return result, nil
}

func stringSetAny(values []string) map[string]bool {
	result := map[string]bool{}
	for _, value := range values {
		result[value] = true
	}
	return result
}
