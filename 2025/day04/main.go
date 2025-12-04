package main

import (
	"flag"
	"math"
	"strconv"
	"strings"

	"aoc/utils"
)

func parseInput(input string) utils.Grid {
	lines := strings.Fields(strings.TrimSpace(input))

	cells := make([][]rune, len(lines))
	for i, line := range lines {
		cells[i] = []rune(line)
	}

	return utils.NewGrid(cells)
}

func countAdjacentRolls(floor utils.Grid, position utils.Position) int {
	adjacentRollCount := 0
	for i := range 4 {
		for _, direction := range []utils.Direction{utils.DIRECTIONS[i], utils.DIRECTIONS[i].Add(utils.DIRECTIONS[(i+1)%4])} {
			adjacentPosition := position.Add(direction)
			if !floor.CheckPosition(adjacentPosition) {
				continue
			}

			if floor.AtPosition(adjacentPosition) == '@' {
				adjacentRollCount++
			}
		}
	}

	return adjacentRollCount
}

func part1(input string) string {
	floor := parseInput(input)

	accessibleRollCount := 0
	for position, cell := range floor.Cells() {
		if cell != '@' {
			continue
		}

		if countAdjacentRolls(floor, position) < 4 {
			accessibleRollCount++
		}
	}

	return strconv.Itoa(accessibleRollCount)
}

func part2(input string) string {
	floor := parseInput(input)

	removedRollCount := 0
	for lastRemovedRollCount := math.MaxInt; lastRemovedRollCount > 0; {
		lastRemovedRollCount = 0

		for position, cell := range floor.Cells() {
			if cell != '@' {
				continue
			}

			if countAdjacentRolls(floor, position) < 4 {
				floor.SetPosition(position, '.')

				removedRollCount++
				lastRemovedRollCount++
			}
		}
	}

	return strconv.Itoa(removedRollCount)
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
