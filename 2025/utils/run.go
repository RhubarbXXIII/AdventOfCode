package utils

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
)

func Run(
	part1 func(string) string,
	part2 func(string) string,
	submit bool,
) {
	_, scriptPath, _, ok := runtime.Caller(1)
	if !ok {
		log.Fatal("Failed to get caller info")
	}

	scriptDirectory := filepath.Dir(scriptPath)

	year := "2025"
	day := parseDay(scriptDirectory)

	sessionCookie := os.Getenv("SESSION_COOKIE")
	if sessionCookie == "" {
		log.Fatal("SESSION_COOKIE environment variable is not set")
	}

	input := fetchInput(scriptDirectory, year, day, sessionCookie)

	result1 := part1(input)
	result2 := part2(input)

	fmt.Printf("Running Day %s:\n", strings.TrimLeft(day, "0"))
	fmt.Printf("  Part 1 Answer: %s\n", result1)
	fmt.Printf("  Part 2 Answer: %s\n", result2)

	// // Submit answers if requested
	// if submit {
	// 	fmt.Println("Submitting answers...")
	// 	SubmitAnswer(year, dayStr, 1, result1)
	// 	SubmitAnswer(year, dayStr, 2, result2)
	// }
}

// Parse day from caller file path.
func parseDay(callingFileDirectory string) string {
	dayDirectory := filepath.Base(callingFileDirectory)
	if len(dayDirectory) < 3 || dayDirectory[:3] != "day" {
		log.Fatalf("Failed to parse day directory: %s", dayDirectory)
	}

	day := dayDirectory[3:]
	if _, ok := strconv.Atoi(day); ok != nil {
		log.Fatalf("Failed to parse day from directory '%s': %s", dayDirectory, day)
	}

	return day
}

// Fetch the input from the input file if there is one, or from the website if not.
func fetchInput(scriptDirectory, year, day, sessionCookie string) string {
	inputPath := filepath.Join(filepath.Dir(filepath.Dir(scriptDirectory)), "input", year, day, "input.txt")

	if _, err := os.Stat(inputPath); err == nil {
		inputBytes, err := os.ReadFile(inputPath)
		if err == nil {
			return string(inputBytes)
		}

		fmt.Printf("Failed to read from input file, retrieving input from website: %v\n", err)
	}

	url := fmt.Sprintf("https://adventofcode.com/%s/day/%s/input", year, strings.TrimLeft(day, "0"))

	request, err := http.NewRequest("GET", url, nil)
	if err != nil {
		log.Fatalf("Failed to create request for input: %v", err)
	}

	request.AddCookie(&http.Cookie{Name: "session", Value: sessionCookie})

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		log.Fatalf("Failed to send request for input: %v", err)
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		log.Fatalf("Unexpected status %d when fetching inputs: %s", response.StatusCode, response.Body)
	}

	inputBytes, err := io.ReadAll(response.Body)
	if err != nil {
		log.Fatalf("Failed to read response body for input: %v", err)
	}

	err = os.Mkdir(filepath.Dir(inputPath), 0644)
	if err != nil {
		log.Printf("Failed to create directory for input file: %v", err)
	}

	err = os.WriteFile(inputPath, inputBytes, 0644)
	if err != nil {
		log.Printf("Failed to write to input file: %v\n", err)
	}

	return string(inputBytes)
}
