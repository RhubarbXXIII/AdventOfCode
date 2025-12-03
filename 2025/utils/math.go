package utils

func Abs(n int) int {
	if n < 0 {
		return -n
	} else {
		return n
	}
}

func Min(a, b int) int {
	if a < b {
		return a
	} else {
		return b
	}
}

func Max(a, b int) int {
	if a > b {
		return a
	} else {
		return b
	}
}
