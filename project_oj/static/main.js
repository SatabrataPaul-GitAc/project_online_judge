function submitCode(){
    const pcode = document.getElementById('pcode')
    const problem_code = pcode.textContent.slice(7)
    console.log(problem_code)
    const submission = document.getElementById('submission')
    const code = submission.value
    console.log(code)
    fetch(`http://localhost:8000/oj/problem/${problem_code}/submit`, {
        method: "POST",
        body: JSON.stringify({
            problem_code: problem_code,
            code: code
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(response => response.json())
    .then((json) => {
        if (json.status === 400){
            console.log(json.message)
            alert(json.message)
        }
	else if (json.status === 200){
            console.log(json.status)
            console.log(json.message)
	    window.location.href="http://localhost:8000/oj/problems/leaderboard"
        }
    })
}
