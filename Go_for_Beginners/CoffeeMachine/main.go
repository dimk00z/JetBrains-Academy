package main

import "fmt"

func main() {
	coffee_algoritm := []string{
		"Starting to make a coffee",
		"Grinding coffee beans",
		"Boiling water",
		"Mixing boiled water with crushed coffee beans",
		"Pouring coffee into the cup",
		"Pouring some milk into the cup",
		"Coffee is ready!",
	}
	for _, line := range coffee_algoritm {
		fmt.Println(line)
	}
}
