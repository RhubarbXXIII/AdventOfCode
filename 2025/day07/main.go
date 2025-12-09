package main

import (
	"flag"
	"strconv"
	"strings"

	"aoc/utils"
)

func parseInput(input string) (manifold utils.Grid, start utils.Position) {
	lines := strings.Fields(strings.TrimSpace(input))

	cells := make([][]rune, len(lines))
	for i, line := range lines {
		cells[i] = []rune(line)
	}

	manifold = utils.NewGrid(cells)

	for i, cell := range manifold.RowAt(0) {
		if cell == 'S' {
			start = utils.NewPosition(0, i)
			break
		}
	}

	return
}

func part1(input string) string {
	manifold, startPosition := parseInput(input)

	splitCount := 0

	beams := map[int]bool{startPosition.Column(): true}

	for _, row := range manifold.Rows() {
		newBeams := map[int]bool{}

		for beam := range beams {
			if row[beam] == '^' {
				newBeams[beam-1] = true
				newBeams[beam+1] = true

				splitCount++
			} else {
				newBeams[beam] = true
			}
		}

		beams = newBeams
	}

	return strconv.Itoa(splitCount)
}

func part2(input string) string {
	manifold, startPosition := parseInput(input)

	pathCounts := map[utils.Position]int{}
	for rowIndex := manifold.RowCount() - 1; rowIndex >= 0; rowIndex-- {
		for columnIndex := 0; columnIndex < manifold.ColumnCount(); columnIndex++ {
			currentPosition := utils.NewPosition(rowIndex, columnIndex)
			nextPosition := currentPosition.Add(utils.DOWN)
			if !manifold.CheckPosition(nextPosition) {
				pathCounts[currentPosition] = 1
				continue
			}

			if manifold.AtPosition(currentPosition) == '^' {
				pathCounts[currentPosition] = pathCounts[nextPosition.Add(utils.LEFT)] + pathCounts[nextPosition.Add(utils.RIGHT)]
			} else {
				pathCounts[currentPosition] = pathCounts[nextPosition]
			}
		}
	}

	return strconv.Itoa(pathCounts[startPosition])
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
