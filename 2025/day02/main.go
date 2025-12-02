package main

import (
	"flag"
	"strconv"
	"strings"

	"aoc/utils"
)

func parseInput(input string) [][2]int {
	idRanges := [][2]int{}

	for idRangeString := range strings.SplitSeq(strings.TrimSpace(input), ",") {
		idRangeSplit := strings.Split(idRangeString, "-")

		idRangeLow, _ := strconv.Atoi(idRangeSplit[0])
		idRangeHigh, _ := strconv.Atoi(idRangeSplit[1])

		idRanges = append(idRanges, [2]int{idRangeLow, idRangeHigh})
	}

	return idRanges
}

func part1(input string) string {
	idRanges := parseInput(input)

	invalidIdSum := 0
	for _, idRange := range idRanges {
		for id := idRange[0]; id <= idRange[1]; id++ {
			idString := strconv.Itoa(id)
			if len(idString)%2 == 1 {
				continue
			}

			if idString[:len(idString)/2] == idString[len(idString)/2:] {
				invalidIdSum += id
			}
		}
	}

	return strconv.Itoa(invalidIdSum)
}

func part2(input string) string {
	idRanges := parseInput(input)

	invalidIdSum := 0
	for _, idRange := range idRanges {
		for id := idRange[0]; id <= idRange[1]; id++ {
			idString := strconv.Itoa(id)

			for size := 1; size <= len(idString)/2; size++ {
				if len(idString)%size != 0 {
					continue
				}

				sequence := idString[:size]
				repeating := true

				for i := 0; i < len(idString)/size; i++ {
					if idString[i*size:(i+1)*size] != sequence {
						repeating = false
						break
					}
				}

				if repeating {
					invalidIdSum += id
					break
				}
			}
		}
	}

	return strconv.Itoa(invalidIdSum)
}

func main() {
	submit := flag.Bool("submit", false, "Submit answers to Advent of Code")
	flag.Parse()

	utils.Run(part1, part2, *submit)
}
