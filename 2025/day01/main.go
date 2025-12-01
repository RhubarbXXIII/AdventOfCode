package main

import (
	"flag"
	"strconv"
	"strings"

	"aoc/utils"
)

func parseInput(input string) []int {
	inputLines := strings.Fields(input)

	rotations := make([]int, len(inputLines))

	for i, line := range inputLines {
		number, _ := strconv.Atoi(line[1:])

		if line[0] == 'L' {
			number *= -1
		}

		rotations[i] = number
	}

	return rotations
}

func part1(input string) string {
	rotations := parseInput(input)

	password := 0

	dial := 50
	for _, rotation := range rotations {
		dial = (dial + rotation + 100) % 100
		if dial == 0 {
			password++
		}
	}

	return strconv.Itoa(password)
}

func part2(input string) string {
	rotations := parseInput(input)

	password := 0

	currentDial := 50
	for _, rotation := range rotations {
		password += utils.Abs(rotation / 100)

		nextDial := ((currentDial+rotation)%100 + 100) % 100

		if nextDial == 0 {
			password++
		} else {
			if currentDial != 0 {
				if rotation < 0 {
					if nextDial > currentDial {
						password++
					}
				} else if rotation > 0 {
					if nextDial < currentDial {
						password++
					}
				}
			}
		}

		currentDial = nextDial
	}

	return strconv.Itoa(password)
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
