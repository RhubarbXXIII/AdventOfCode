package main

import (
	"flag"
	"math"
	"slices"
	"strconv"
	"strings"

	"aoc/utils"
)

func parseInput(input string) [][]int {
	inputLines := strings.Fields(strings.TrimSpace(input))

	banks := make([][]int, len(inputLines))
	for i, line := range inputLines {
		banks[i] = make([]int, len(line))
		for j, battery := range strings.Split(line, "") {
			banks[i][j], _ = strconv.Atoi(battery)
		}
	}

	return banks
}

func part1(input string) string {
	banks := parseInput(input)

	joltage := 0
	for _, bank := range banks {
		firstDigit := -1
		secondDigit := -1

		for i, battery := range bank {
			if i < len(bank)-1 && battery > firstDigit {
				firstDigit = battery
				secondDigit = -1
				continue
			}

			if battery > secondDigit {
				secondDigit = battery
			}
		}

		joltage += 10*firstDigit + secondDigit
	}

	return strconv.Itoa(joltage)
}

func part2(input string) string {
	banks := parseInput(input)

	joltage := 0
	for _, bank := range banks {
		digits := slices.Repeat([]int{-1}, 12)
		digitCountRemaining := 12

		for i, battery := range bank {
			for j := utils.Max(12-(len(bank)-i), 0); j < 12; j++ {
				if battery > digits[j] {
					digits[j] = battery

					digitCountRemaining = 11 - j
					copy(digits[j+1:], slices.Repeat([]int{-1}, digitCountRemaining))

					break
				}
			}
		}

		for i, digit := range digits {
			joltage += int(math.Pow10(11-i)) * digit
		}
	}

	return strconv.Itoa(joltage)
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
