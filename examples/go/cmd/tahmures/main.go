package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/mehdikhoshtinat/tahmures/examples/go/tahmures"
)

func main() {
	if len(os.Args) < 2 || os.Args[1] != "run" {
		fmt.Fprintln(os.Stderr, "usage: tahmures run --manifest PATH [--output PATH]")
		os.Exit(2)
	}
	flags := flag.NewFlagSet("run", flag.ExitOnError)
	manifestPath := flags.String("manifest", "", "experiment manifest")
	outputPath := flags.String("output", "", "optional report path")
	clientName := flags.String("client", "fixture", "client implementation")
	if err := flags.Parse(os.Args[2:]); err != nil {
		fail(err)
	}
	if *manifestPath == "" || *clientName != "fixture" {
		fail(fmt.Errorf("--manifest is required and only --client fixture is supported"))
	}
	manifest, err := tahmures.LoadManifest(*manifestPath)
	if err != nil {
		fail(err)
	}
	fixtures, err := tahmures.LoadFixtures(
		tahmures.ResolveProjectPath(*manifestPath, manifest.Fixtures),
	)
	if err != nil {
		fail(err)
	}
	runner := tahmures.ExperimentRunner{
		Manifest:     manifest,
		ManifestPath: *manifestPath,
		Client:       tahmures.NewFixtureClient(fixtures),
	}
	report, err := runner.Run(context.Background())
	if err != nil {
		fail(err)
	}
	payload, err := json.MarshalIndent(report, "", "  ")
	if err != nil {
		fail(err)
	}
	payload = append(payload, '\n')
	if *outputPath == "" {
		_, err = os.Stdout.Write(payload)
	} else {
		err = os.WriteFile(*outputPath, payload, 0o644)
	}
	if err != nil {
		fail(err)
	}
}

func fail(err error) {
	fmt.Fprintf(os.Stderr, "error: %v\n", err)
	os.Exit(2)
}
