package main

import (
	"flag"
	"slices"
	"strconv"
	"strings"

	"aoc/utils"
)

func parseInput(input string) (freshRanges [][2]int64, ingredients []int64) {
	lines := strings.Fields(strings.TrimSpace(input))

	for _, line := range lines {
		if ingredient, err := strconv.ParseInt(line, 10, 64); err == nil {
			ingredients = append(ingredients, ingredient)
		} else if strings.Contains(line, "-") {
			lineSplit := strings.Split(line, "-")

			freshRangeLow, _ := strconv.ParseInt(lineSplit[0], 10, 64)
			freshRangeHigh, _ := strconv.ParseInt(lineSplit[1], 10, 64)
			freshRanges = append(freshRanges, [2]int64{freshRangeLow, freshRangeHigh})
		}
	}

	return
}

func part1(input string) string {
	freshRanges, ingredients := parseInput(input)

	freshIngredientCount := 0
	for _, ingredient := range ingredients {
		for _, freshRange := range freshRanges {
			if freshRange[0] <= ingredient && ingredient <= freshRange[1] {
				freshIngredientCount++
				break
			}
		}
	}

	return strconv.Itoa(freshIngredientCount)
}

func part2(input string) string {
	freshRanges, _ := parseInput(input)

	slices.SortFunc(freshRanges, func(left, right [2]int64) int {
		if left[0] < right[0] {
			return -1
		} else if left[0] > right[0] {
			return 1
		} else if left[1] < right[1] {
			return -1
		} else if left[1] > right[1] {
			return 1
		} else {
			return 0
		}
	})

	var freshIngredientCount int64 = 0

	var lastIngredient int64 = -1
	for _, freshRange := range freshRanges {
		if lastIngredient < freshRange[0] {
			freshIngredientCount += freshRange[1] - freshRange[0] + 1
		} else if lastIngredient < freshRange[1] {
			freshIngredientCount += freshRange[1] - lastIngredient
		} else {
			continue
		}

		lastIngredient = freshRange[1]
	}

	return strconv.FormatInt(freshIngredientCount, 10)
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
