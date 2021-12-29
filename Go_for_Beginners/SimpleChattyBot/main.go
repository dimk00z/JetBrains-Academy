package main

import "fmt"

func main() {
	var bot_name string = "Aid"
	var birth_year int = 2021
	fmt.Printf("Hello! My name is %s\n", bot_name)
	fmt.Printf("I was created in %d.\n", birth_year)
	fmt.Println("Please, remind me your name.")
	var user_name string
	fmt.Scan(&user_name)
	fmt.Printf("What a great name you have, %s!", user_name)
}
