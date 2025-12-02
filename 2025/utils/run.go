package utils

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
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

	fmt.Printf("Running Day %s:\n", strings.TrimLeft(day, "0"))

	result1 := part1(input)
	fmt.Printf("  Part 1 Answer: %s\n", result1)
	if submit && result1 != "" {
		correct, response := submitAnswer(year, day, "1", result1, sessionCookie)
		if correct {
			fmt.Printf("    %s\n", response)
		} else {
			log.Printf("    %s\n", response)
		}
	}

	result2 := part2(input)
	fmt.Printf("  Part 2 Answer: %s\n", result2)
	if submit && result2 != "" {
		correct, response := submitAnswer(year, day, "2", result2, sessionCookie)
		if correct {
			fmt.Printf("    %s\n", response)
		} else {
			log.Printf("    %s\n", response)
		}
	}
}

// Parse the day from the script directory.
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

	urlString := fmt.Sprintf("https://adventofcode.com/%s/day/%s/input", year, strings.TrimLeft(day, "0"))

	request, err := http.NewRequest("GET", urlString, nil)
	if err != nil {
		log.Fatalf("Failed to create request for fetching input: %v", err)
	}

	request.AddCookie(&http.Cookie{Name: "session", Value: sessionCookie})

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		log.Fatalf("Failed to send request for fetching input: %v", err)
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		log.Fatalf("Unexpected status %d when fetching input: %s", response.StatusCode, response.Body)
	}

	inputBytes, err := io.ReadAll(response.Body)
	if err != nil {
		log.Fatalf("Failed to read response body for fetching input: %v", err)
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

// Submit an answer to the website.
func submitAnswer(year, day, part, answer, sessionCookie string) (bool, string) {
	urlString := fmt.Sprintf("https://adventofcode.com/%s/day/%s/answer", year, strings.TrimLeft(day, "0"))

	form := url.Values{}
	form.Set("level", part)
	form.Set("answer", answer)

	request, err := http.NewRequest("POST", urlString, strings.NewReader(form.Encode()))
	if err != nil {
		log.Fatalf("Failed to create request for submitting answer: %v", err)
	}

	request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	request.AddCookie(&http.Cookie{Name: "session", Value: sessionCookie})

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		log.Fatalf("Failed to send request for submitting answer: %v", err)
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		log.Fatalf("Unexpected status %d when submitting answer: %s", response.StatusCode, response.Body)
	}

	resultBytes, err := io.ReadAll(response.Body)
	if err != nil {
		log.Fatalf("Failed to read response body for submitting answer: %v", err)
	}

	result := strings.ToLower(string(resultBytes))

	if strings.Contains(result, "that's the right answer") {
		return true, "Submitted correct answer!"
	} else if strings.Contains(result, "too low") {
		return false, "Submitted answer was too low."
	} else if strings.Contains(result, "too high") {
		return false, "Submitted answer was too high."
	} else if strings.Contains(result, "not the right answer") {
		return false, "Submitted answer was incorrect."
	} else if strings.Contains(result, "too recently") {
		return false, "Submitted answer too recently."
	} else if strings.Contains(result, "already got") || strings.Contains(result, "solving the right level") {
		return true, "Already submitted correct answer."
	} else {
		return false, fmt.Sprintf("Unrecognized response message: %s", result)
	}
}
