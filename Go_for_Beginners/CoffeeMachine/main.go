package main

import (
	"fmt"
	"log"
)

type CoffeeMachine struct {
	money          int
	water          int
	milk           int
	coffee         int
	disposableCups int
}

func getUserInt() (userInput int) {
	_, err := fmt.Scanf("%d", &userInput)
	if err != nil {
		log.Fatal(err)
	}
	return userInput
}
func (coffeeMachine *CoffeeMachine) printState() {
	fmt.Printf(`The coffee machine has:
%d of water
%d of milk
%d of coffee beans
%d of disposable cups
%d of money
`, coffeeMachine.water, coffeeMachine.milk, coffeeMachine.coffee, coffeeMachine.disposableCups, coffeeMachine.money)
}
func (coffeeMachine *CoffeeMachine) buyCoffee() {
	fmt.Println("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
	var userInput int = getUserInt()
	switch userInput {
	case 1:
		coffeeMachine.water -= 250
		coffeeMachine.coffee -= 16
		coffeeMachine.money += 4
		coffeeMachine.disposableCups--
	case 2:
		coffeeMachine.water -= 350
		coffeeMachine.coffee -= 20
		coffeeMachine.money += 7
		coffeeMachine.milk -= 75
		coffeeMachine.disposableCups--
	case 3:
		coffeeMachine.water -= 200
		coffeeMachine.coffee -= 12
		coffeeMachine.money += 6
		coffeeMachine.milk -= 100
		coffeeMachine.disposableCups--
	}
}
func addUserIntInput(question string, value *int) {
	fmt.Println(question)
	var additionalValue int = getUserInt()
	*value = *value + additionalValue
}
func (coffeeMachine *CoffeeMachine) fillIngredients() {
	addUserIntInput("Write how many ml of water you want to add:", &coffeeMachine.water)
	addUserIntInput("Write how many ml of milk you want to add:", &coffeeMachine.milk)
	addUserIntInput("Write how many grams of coffee beans you want to add:", &coffeeMachine.coffee)
	addUserIntInput("Write how many disposable coffee cups you want to add:", &coffeeMachine.disposableCups)

}
func (coffeeMachine *CoffeeMachine) takeMoney() {
	fmt.Printf("I gave you $%d\n", coffeeMachine.money)
	coffeeMachine.money = 0
}
func newInitCoffeeMachine() CoffeeMachine {
	return CoffeeMachine{
		water:          400,
		milk:           540,
		coffee:         120,
		disposableCups: 9,
		money:          550}
}
func buyFillTake() {
	var coffeeMachine CoffeeMachine = newInitCoffeeMachine()
	coffeeMachine.printState()
	fmt.Println("Write action (buy, fill, take):")
	var userChoice string
	fmt.Scanf("%s", &userChoice)
	switch userChoice {
	case "buy":
		coffeeMachine.buyCoffee()
	case "fill":
		coffeeMachine.fillIngredients()
	case "take":
		coffeeMachine.takeMoney()
	}
	coffeeMachine.printState()

}
func main() {
	buyFillTake()
}
