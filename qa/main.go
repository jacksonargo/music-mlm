package main

import (
	"bytes"
	"encoding/csv"
	"encoding/json"
	"log"
	"music-production-qa/qa/textbook"
	"os"
	"strconv"
)

type flatData struct {
	Context     string `json:"context"`
	Question    string `json:"question"`
	Answer      string `json:"answers.text"`
	AnswerStart int    `json:"answers.answers_start"`
}

func main() {
	data := flattenTextbookData(textbook.Data)
	writeJSON(data, "output.jsonl")
	writeCSV(data, "output.csv")
}

func writeCSV(data []flatData, dest string) {
	var bufCsv bytes.Buffer
	csvWriter := csv.NewWriter(&bufCsv)
	if err := csvWriter.Write([]string{"context", "question", "answers.text", "answers.answers_start"}); err != nil {
		log.Fatalln(err)
	}
	for _, row := range data {
		if err := csvWriter.Write([]string{
			row.Context, row.Question, row.Answer, strconv.Itoa(row.AnswerStart),
		}); err != nil {
			log.Fatalln(err)
		}
	}
	if err := os.WriteFile(dest, bufCsv.Bytes(), 0644); err != nil {
		log.Fatalln(err)
	}
}

func writeJSON(data []flatData, dest string) {
	var buf bytes.Buffer
	encoder := json.NewEncoder(&buf)
	for _, row := range data {
		if err := encoder.Encode(flatData{
			Context:     row.Context,
			Question:    row.Question,
			Answer:      row.Answer,
			AnswerStart: row.AnswerStart,
		}); err != nil {
			log.Fatalln(err)
		}
	}
	if err := os.WriteFile(dest, buf.Bytes(), 0644); err != nil {
		log.Fatalln(err)
	}
}

func flattenTextbookData(input []textbook.Textbook) []flatData {
	var data []flatData
	for _, book := range input {
		for _, context := range book.Contexts {
			if context.Text == "" {
				continue
			}
			for _, q := range context.Questions {
				data = append(data, flatData{
					Context:     context.Text,
					Question:    q.Question,
					Answer:      q.Answer,
					AnswerStart: q.AnswerStartsAt,
				})
			}
		}
	}
	return data
}
