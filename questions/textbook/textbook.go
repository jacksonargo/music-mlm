package textbook

type Textbook struct {
	Name     string
	Contexts []QuestionContext
}

type QuestionContext struct {
	Text      string
	Questions []QuestionAnswer
}

type QuestionAnswer struct {
	Question       string
	Answer         string
	AnswerStartsAt int
}

var Data []Textbook // this populated by data.go
