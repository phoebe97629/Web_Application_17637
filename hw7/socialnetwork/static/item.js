function getList() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }
    console.log("getList")
    xhr.open("GET", "/socialnetwork/get-global", true)
    xhr.send()
}

function getFollowerList() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updateFollowerPage(xhr)
    }
    console.log("getFollowerList")
    xhr.open("GET", "/socialnetwork/get-follower", true)
    xhr.send()
}



function updatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response)
        // console.log('updatePage')
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function updateFollowerPage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateFollowerList(response)
        // console.log('updatePage')
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateList(items) {
    // Removes the old to-do list items
    let list = document.getElementById("commnet-list")

    for (let i = 0; i < items['post'].length; i++) {

        let item = items['post'][i]
        let element = document.createElement("div")
        element.id = 'id_post_div_' + item.post_id
        element.style.fontSize = '30px'

        if (document.getElementById('id_post_div_' + item.post_id) == null){
            // console.log('Test')
            let name_link = document.createElement("a")
            name_link.href = "/socialnetwork/other_profile/" + item.user_id
            name_link.id = 'id_post_profile_' + item.post_id
            name_link.innerHTML = "Post by " + item.first + item.last
            name_link.style.color = "#DB7B65"

            let post_text = document.createElement("p")
            post_text.id = 'id_post_text_' + item.post_id
            post_text.innerHTML = sanitize(item.text)

            var time = new Date(item.time)
            let spanTime = document.createElement("span")
                    spanTime.id = "id_post_date_time_" + item.post_id
                    spanTime.innerHTML = time.toLocaleDateString('en-US') + " " + time.toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit'
                    })
                    spanTime.style.fontStyle = "italic"


            let label = document.createElement('label')
            label.innerHTML = 'Comment:'

            let input = document.createElement('input')
            input.type = 'text'
            input.id = 'id_comment_input_text_' + item.post_id

            let space = document.createElement('br')

            let commentButton = document.createElement('button')
            commentButton.innerHTML = 'Submit'
            commentButton.id = 'id_comment_button_' + item.post_id
            commentButton.onclick = function(){addComment(item.post_id)}

            let comment_list = document.createElement('div')
            comment_list.id = 'comments_under_here' + item.post_id
            comment_list.style.margin = "30px"

            element.appendChild(name_link)
            element.appendChild(post_text)
            element.appendChild(spanTime)
            element.appendChild(space)
            element.appendChild(comment_list)
            element.appendChild(label)
            element.appendChild(input)
            element.appendChild(commentButton)
            list.prepend(element)
            
        }
    }

    for (let i = 0; i < items['comment'].length; i++){
        let comment_item = items['comment'][i]
        let comment_element = document.createElement('div')
        console.log('HHH')
        let post_div = document.getElementById("comments_under_here" + comment_item.post_id)
        comment_element.id = 'id_comment_div_' + comment_item.comm_id

        if (document.getElementById('id_comment_div_' + comment_item.comm_id) == null){

            let comment_name_link = document.createElement("a")
            comment_name_link.href = "/socialnetwork/other_profile/" + comment_item.user_id
            comment_name_link.id = 'id_comment_profile_' + comment_item.comm_id
            comment_name_link.innerHTML = "Comment by: " + comment_item.first + comment_item.last
            comment_name_link.style.color = '#FBC9BE'

            let comment_text = document.createElement("p")
            comment_text.id = 'id_comment_text_' + comment_item.comm_id
            comment_text.innerHTML = sanitize(comment_item.comment)

            var comment_time = new Date(comment_item.time)
            let comment_spanTime = document.createElement("span")
                    comment_spanTime.id = "id_comment_date_time_" + comment_item.comm_id
                    comment_spanTime.innerHTML = comment_time.toLocaleDateString('en-US') + " " + comment_time.toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit'
                    })
                    comment_spanTime.style.fontStyle = "italic"

            // console.log(comment_time)
            comment_element.appendChild(comment_name_link)
            comment_element.appendChild(comment_text)
            comment_element.appendChild(comment_spanTime)
            console.log('HHH')
            post_div.appendChild(comment_element)
    }}
}

function updateFollowerList(items) {
    // Removes the old to-do list items
    let list = document.getElementById("follower-comment-list")

    for (let i = 0; i < items['post'].length; i++) {

        let item = items['post'][i]
        let element = document.createElement("div")
        element.id = 'id_post_div_' + item.post_id
        element.style.fontSize = '30px'

        if (document.getElementById('id_post_div_' + item.post_id) == null){
            // console.log('Test')
            let name_link = document.createElement("a")
            name_link.href = "/socialnetwork/other_profile/" + item.user_id
            name_link.id = 'id_post_profile_' + item.post_id
            name_link.innerHTML = "Post by " + item.first + item.last
            name_link.style.color = "#DB7B65"

            let post_text = document.createElement("p")
            post_text.id = 'id_post_text_' + item.post_id
            post_text.innerHTML = sanitize(item.text)

            var time = new Date(item.time)
            let spanTime = document.createElement("span")
                    spanTime.id = "id_post_date_time_" + item.post_id
                    spanTime.innerHTML = time.toLocaleDateString('en-US') + " " + time.toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit'
                    })
                    spanTime.style.fontStyle = "italic"


            let label = document.createElement('label')
            label.innerHTML = 'Comment:'

            let input = document.createElement('input')
            input.type = 'text'
            input.id = 'id_comment_input_text_' + item.post_id

            let space = document.createElement('br')

            let commentButton = document.createElement('button')
            commentButton.innerHTML = 'Submit'
            commentButton.id = 'id_comment_button_' + item.post_id
            commentButton.onclick = function(){addFollowerComment(item.post_id)}

            let comment_list = document.createElement('div')
            comment_list.id = 'comments_under_here' + item.post_id
            comment_list.style.margin = "30px"

            element.appendChild(name_link)
            element.appendChild(post_text)
            element.appendChild(spanTime)
            element.appendChild(space)
            element.appendChild(comment_list)
            element.appendChild(label)
            element.appendChild(input)
            element.appendChild(commentButton)
            list.prepend(element)
            
        }
    }

    for (let i = 0; i < items['comment'].length; i++){
        let comment_item = items['comment'][i]
        let comment_element = document.createElement('div')
        console.log('HHH')
        let post_div = document.getElementById("comments_under_here" + comment_item.post_id)
        comment_element.id = 'id_comment_div_' + comment_item.comm_id

        if (document.getElementById('id_comment_div_' + comment_item.comm_id) == null){

            let comment_name_link = document.createElement("a")
            comment_name_link.href = "/socialnetwork/other_profile/" + comment_item.user_id
            comment_name_link.id = 'id_comment_profile_' + comment_item.comm_id
            comment_name_link.innerHTML = "Comment by: " + comment_item.first + comment_item.last
            comment_name_link.style.color = '#FBC9BE'

            let comment_text = document.createElement("p")
            comment_text.id = 'id_comment_text_' + comment_item.comm_id
            comment_text.innerHTML = sanitize(comment_item.comment)

            var comment_time = new Date(comment_item.time)
            let comment_spanTime = document.createElement("span")
                    comment_spanTime.id = "id_comment_date_time_" + comment_item.comm_id
                    comment_spanTime.innerHTML = comment_time.toLocaleDateString('en-US') + " " + comment_time.toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit'
                    })
                    comment_spanTime.style.fontStyle = "italic"

            // console.log(comment_time)
            comment_element.appendChild(comment_name_link)
            comment_element.appendChild(comment_text)
            comment_element.appendChild(comment_spanTime)
            console.log('HHH')
            post_div.appendChild(comment_element)
    }}
}


function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function addItem() {
    let itemTextElement = document.getElementById("id_post_input_text")
    let itemTextValue   = itemTextElement.value

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        console.log('addItem Updatepage')
        updatePage(xhr)
        // console.log('addItem Updatepage')
    }

    xhr.open("POST", addItemURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

function addComment(post_id) {
    console.log("hhh: " + post_id)
    let itemTextElement = document.getElementById('id_comment_input_text_' + post_id)
    let itemTextValue   = itemTextElement.value

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addCommentURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("comment_text="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken() + '&post_id='+post_id);
}

function addFollowerComment(post_id) {
    // console.log("hhh: " + post_id)
    let itemTextElement = document.getElementById('id_comment_input_text_' + post_id)
    let itemTextValue   = itemTextElement.value

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addFollowerCommentURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("comment_text="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken() + '&post_id='+post_id);
}



function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}