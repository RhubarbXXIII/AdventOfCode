package main

import (
	"flag"
	"slices"
	"strconv"
	"strings"

	"aoc/utils"
)

type position3d struct {
	x, y, z int
}

func (this position3d) distanceSquaredTo(other position3d) int {
	return (other.x-this.x)*(other.x-this.x) + (other.y-this.y)*(other.y-this.y) + (other.z-this.z)*(other.z-this.z)
}

func parseInput(input string) []position3d {
	lines := strings.Fields(strings.TrimSpace(input))

	positions := make([]position3d, len(lines))
	for i, line := range lines {
		lineSplit := strings.Split(line, ",")

		position := position3d{}
		position.x, _ = strconv.Atoi(lineSplit[0])
		position.y, _ = strconv.Atoi(lineSplit[1])
		position.z, _ = strconv.Atoi(lineSplit[2])

		positions[i] = position
	}

	return positions
}

func part1(input string) string {
	boxes := parseInput(input)

	pairs := [][2]position3d{}
	for i, left := range boxes {
		for _, right := range boxes[i+1:] {
			pairs = append(pairs, [2]position3d{left, right})
		}
	}

	slices.SortFunc(pairs, func(left, right [2]position3d) int {
		return left[0].distanceSquaredTo(left[1]) - right[0].distanceSquaredTo(right[1])
	})

	circuits := []map[position3d]bool{}

	for _, pair := range pairs[:1000] {
		leftCircuitIndex, rightCircuitIndex := -1, -1
		for circuitIndex, circuit := range circuits {
			if _, present := circuit[pair[0]]; present {
				leftCircuitIndex = circuitIndex
			}
			if _, present := circuit[pair[1]]; present {
				rightCircuitIndex = circuitIndex
			}
		}

		if leftCircuitIndex >= 0 && leftCircuitIndex == rightCircuitIndex {
			continue
		} else if leftCircuitIndex == -1 && rightCircuitIndex == -1 {
			circuits = append(circuits, map[position3d]bool{pair[0]: true, pair[1]: true})
		} else if leftCircuitIndex == -1 {
			circuits[rightCircuitIndex][pair[0]] = true
		} else if rightCircuitIndex == -1 {
			circuits[leftCircuitIndex][pair[1]] = true
		} else {
			for box := range circuits[rightCircuitIndex] {
				circuits[leftCircuitIndex][box] = true
			}

			circuits[rightCircuitIndex] = circuits[len(circuits)-1]
			circuits = circuits[:len(circuits)-1]
		}
	}

	slices.SortFunc(circuits, func(left, right map[position3d]bool) int {
		return len(right) - len(left)
	})

	circuitProduct := 1
	for i := range 3 {
		circuitProduct *= len(circuits[i])
	}

	return strconv.Itoa(circuitProduct)
}

func part2(input string) string {
	boxes := parseInput(input)

	pairs := [][2]position3d{}
	for i, left := range boxes {
		for _, right := range boxes[i+1:] {
			pairs = append(pairs, [2]position3d{left, right})
		}
	}

	slices.SortFunc(pairs, func(left, right [2]position3d) int {
		return left[0].distanceSquaredTo(left[1]) - right[0].distanceSquaredTo(right[1])
	})

	boxesSeen := map[position3d]bool{}
	circuits := []map[position3d]bool{}

	for _, pair := range pairs {
		leftCircuitIndex, rightCircuitIndex := -1, -1
		for circuitIndex, circuit := range circuits {
			if _, present := circuit[pair[0]]; present {
				leftCircuitIndex = circuitIndex
			}
			if _, present := circuit[pair[1]]; present {
				rightCircuitIndex = circuitIndex
			}
		}

		if leftCircuitIndex >= 0 && leftCircuitIndex == rightCircuitIndex {
			continue
		} else if leftCircuitIndex == -1 && rightCircuitIndex == -1 {
			circuits = append(circuits, map[position3d]bool{pair[0]: true, pair[1]: true})
		} else if leftCircuitIndex == -1 {
			circuits[rightCircuitIndex][pair[0]] = true
		} else if rightCircuitIndex == -1 {
			circuits[leftCircuitIndex][pair[1]] = true
		} else {
			for box := range circuits[rightCircuitIndex] {
				circuits[leftCircuitIndex][box] = true
			}

			circuits[rightCircuitIndex] = circuits[len(circuits)-1]
			circuits = circuits[:len(circuits)-1]
		}

		boxesSeen[pair[0]] = true
		boxesSeen[pair[1]] = true

		if len(boxesSeen) == len(boxes) && len(circuits) == 1 {
			return strconv.Itoa(pair[0].x * pair[1].x)
		}
	}

	panic("Circuit never completed!")
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
