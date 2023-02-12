const quizData1 = []
const quizData = [
    {
        question: "Which language runs in a web browser?",
        a: "Java",
        b: "C",
        c: "Python",
        d: "javascript",
        correct: "d",
    }
];
getQuestions()

const quiz= document.getElementById('quiz')
const answerEls = document.querySelectorAll('.answer')
const questionEl = document.getElementById('question')
const a_text = document.getElementById('a_text')
const b_text = document.getElementById('b_text')
const c_text = document.getElementById('c_text')
const d_text = document.getElementById('d_text')
const submitBtn = document.getElementById('submit')


let currentQuiz = 0
let score = 0
loadQuiz()

function loadQuiz() {

    deselectAnswers()

    const currentQuizData = quizData[currentQuiz]

    questionEl.innerText = currentQuizData.question
    a_text.innerText = currentQuizData.a
    b_text.innerText = currentQuizData.b
    c_text.innerText = currentQuizData.c
    d_text.innerText = currentQuizData.d
}

function deselectAnswers() {
    answerEls.forEach(answerEl => answerEl.checked = false)
}

function getSelected() {
    let answer
    answerEls.forEach(answerEl => {
        if(answerEl.checked) {
            answer = answerEl.id
        }
    })
    return answer
}


submitBtn.addEventListener('click', () => {
    const answer = getSelected()
    if(answer) {
       if(answer === quizData[currentQuiz].correct) {
           score++
       }

       currentQuiz++

       if(currentQuiz < quizData.length) {
           loadQuiz()
       } else {
           quiz.innerHTML = `
           <h2>You answered ${score}/${quizData.length} questions correctly</h2>

           <button onclick="location.reload()">Reload</button>
           `
       }
    }
})

function getQuestions(){

        url='https://the-trivia-api.com/api/questions'
        fetch(url)
          .then((response) => response.json())
          .then((data) => {
            for(let item=1; item<data.length; item++){
            let options = ["a", "b", "c", "d"];

            let cor_op = Math.floor(Math.random() * options.length);
            console.log(cor_op, options[cor_op]);

            let quiz_item ={
                          question: data[item].question,
                          correct: options[cor_op],
                      }
              quiz_item[options[cor_op]]=data[item].correctAnswer
              options = options.filter(item => item !== options[cor_op])
              console.log(options)

              for(let op=0; op<options.length; op++){
                quiz_item[options[op]]=data[item].incorrectAnswers[op]

              }
              quizData.push(quiz_item)
            }
            console.log(quizData)
            console.log(quizData1)

            });

    };