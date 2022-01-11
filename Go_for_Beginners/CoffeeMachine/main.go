package main

import (
	"fmt"
	"log"
)

func printCoffeeAlgoritm() {
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
func calculateIngredients() {
	var cups int
	fmt.Println("Write how many cups of coffee you will need:")
	_, err := fmt.Scanf("%d", &cups)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("For %d cups of coffee you will need:\n", cups)
	fmt.Printf("%d ml of water\n", cups*200)
	fmt.Printf("%d ml of milk\n", cups*50)
	fmt.Printf("%d g of coffee beans\n", cups*15)
}
func main() {
	printCoffeeAlgoritm()
	calculateIngredients()
}
