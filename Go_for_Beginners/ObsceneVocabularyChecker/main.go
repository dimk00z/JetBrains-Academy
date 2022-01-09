package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func readWords(file_name *string) (forbidden_words map[string]bool) {
	file, err := os.Open(*file_name)
	if err != nil {
		log.Fatal((err))
		return
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanWords)
	forbidden_words = make(map[string]bool)
	for scanner.Scan() {
		forbidden_words[strings.ToLower(scanner.Text())] = true
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return
}

func checkWord(word *string, forbidden_words *map[string]bool) bool {
	if _, ok := (*forbidden_words)[strings.ToLower(*word)]; ok {
		return true
	}
	return false
}

func wordToStars(word *string) string {
	return strings.Repeat("*", len(*word))
}

func correctSentence(sentence *string, forbidden_words *map[string]bool) string {
	words := strings.Split(*sentence, " ")

	for wordPosition, word := range words {
		if checkWord(&word, forbidden_words) {
			words[wordPosition] = wordToStars(&word)
		}
	}
	return strings.Join(words, " ")
}

func main() {
	var file_name string
	fmt.Scanf("%s", &file_name)
	forbidden_words := readWords(&file_name)
	var sentence string
	scanner := bufio.NewScanner(os.Stdin)
	for {
		scanner.Scan()
		if strings.ToLower(scanner.Text()) == "exit" {
			break
		}
		sentence = scanner.Text()
		fmt.Printf("%s\n", correctSentence(&sentence, &forbidden_words))
	}
	fmt.Println("Bye!")
}
