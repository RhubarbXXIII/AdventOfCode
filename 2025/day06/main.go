package main

import (
	"flag"
	"strconv"
	"strings"

	"aoc/utils"
)

func parseInput(input string) (rows [][]int, operations []rune) {
	lines := strings.Split(strings.TrimSpace(input), "\n")

	rows = make([][]int, len(lines)-1)

	for i, line := range lines {
		cells := strings.Fields(strings.TrimSpace(line))

		_, err := strconv.Atoi(cells[0])
		if err != nil {
			operations = make([]rune, len(cells))
			for j, operation := range cells {
				operations[j] = rune(operation[0])
			}

			continue
		}

		rows[i] = make([]int, len(cells))
		for j, cell := range cells {
			rows[i][j], _ = strconv.Atoi(cell)
		}
	}

	return
}

func part1(input string) string {
	lines := strings.Split(strings.TrimSpace(input), "\n")

	rows := make([][]int, len(lines)-1)
	var operations []rune

	for i, line := range lines {
		cells := strings.Fields(strings.TrimSpace(line))

		_, err := strconv.Atoi(cells[0])
		if err != nil {
			operations = make([]rune, len(cells))
			for j, operation := range cells {
				operations[j] = rune(operation[0])
			}

			continue
		}

		rows[i] = make([]int, len(cells))
		for j, cell := range cells {
			rows[i][j], _ = strconv.Atoi(cell)
		}
	}

	total := 0

	for i := range rows[0] {
		operation := operations[i]

		var result int
		if operation == '*' {
			result = 1
		}

		for j := range rows {
			switch operation {
			case '+':
				result += rows[j][i]
			case '*':
				result *= rows[j][i]
			}
		}

		total += result
	}

	return strconv.Itoa(total)
}

func part2(input string) string {
	lines := strings.Split(input, "\n")
	for lines[len(lines)-1] == "" {
		lines = lines[:len(lines)-1]
	}

	total := 0

	operationLine := lines[len(lines)-1]
	for operationIndex := 0; operationIndex < len(operationLine); {
		operation := operationLine[operationIndex]

		var nextOperationIndex int
		plusIndex := strings.Index(operationLine[operationIndex+1:], "+")
		timesIndex := strings.Index(operationLine[operationIndex+1:], "*")
		if plusIndex == -1 && timesIndex == -1 {
			nextOperationIndex = len(operationLine)
		} else if plusIndex == -1 {
			nextOperationIndex = timesIndex + operationIndex + 1
		} else if timesIndex == -1 {
			nextOperationIndex = plusIndex + operationIndex + 1
		} else {
			nextOperationIndex = utils.Min(plusIndex, timesIndex) + operationIndex + 1
		}

		var result = 0
		if operation == '*' {
			result = 1
		}

		for i := operationIndex; i < nextOperationIndex; i++ {
			operand := 0
			magnitude := 1

			for j := len(lines) - 2; j >= 0; j-- {
				digit, err := strconv.Atoi(string(lines[j][i]))
				if err == nil {
					operand += digit * magnitude
					magnitude *= 10
				}
			}

			if operand == 0 {
				continue
			}

			switch operation {
			case '+':
				result += operand
			case '*':
				result *= operand
			}
		}

		total += result

		operationIndex = nextOperationIndex
	}

	return strconv.Itoa(total)
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
