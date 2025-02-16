let allData = [];
const autoCompleteInputs = document.querySelectorAll(".autoComplete");
const createBtn = document.querySelectorAll(".createBtn");
const tasksLists = document.querySelectorAll(".tasks");


async function fetchTasksList(listId) {
    try {
        const response = await fetch(`/lists/${listId}/tasks`);
        const data = await response.json();
        console.log("Data loaded:", data);
        return data.tasks;
    } catch (error) {
        console.error("Error loading data:", error);
    }
}


async function displayTasks() {
    for (const tasksList of tasksLists) {
        tasksList.innerHTML = "";
        const listId = tasksList.getAttribute("data-list-id");
        const tasks = fetchTasksList(listId);

        tasks.then((data) => {
            // console.log("Data loaded:", data);
            for (const task of data) {
                const taskElement = document.createElement("div");
                taskElement.classList.add("task");
                taskElement.innerHTML = `
                <input type="checkbox" id="task-${task}" />
                <label for="task-${task}">${task}</label>`;
                tasksList.appendChild(taskElement);
            }
        });
    }
}

async function preloadData() {
    try {
        const response = await fetch("/tasks/");
        const data = await response.json();
        // console.log("Data loaded:", data);
        allData = data.tasks;
        // console.log("Data loaded:", allData);
        initializeAutoComplete();
    } catch (error) {
        // console.error("Error loading data:", error);
    }
}

function initializeAutoComplete() {
    for (const input of autoCompleteInputs) {
        let listId = input.getAttribute("data-list-id");
        let selector = `#autoComplete-${listId}`;
        const autoCompleteJS = new autoComplete({
            selector: selector,
            data: {
                src: allData,
            },
            resultItem: {
                highlight: true,
            },
            events: {
                input: {
                    selection: (event) => {
                        const selection = event.detail.selection.value;
                        console.log(selector);
                        let listId = input.getAttribute("data-list-id");
                        document.querySelector(selector).value = selection;
                        addTaskToList(selection, listId);
                        displayTasks();
                    },
                },
            },
        });
    }
}

for (const btn of createBtn) {
    btn.addEventListener("click", (event) => {
        let listId = btn.getAttribute("data-list-id");
        let selector = `#autoComplete-${listId}`;
        let value = document.querySelector(selector).value;
        createAndAddTaskToList(value, listId);

    });
}


async function addTaskToList(query, listId) {
    // console.log(`Sending AJAX request for: ${query}`);
    try {
        const response = await fetch(`/lists/${listId}/add_task/${query}`);
        const result = await response.json();
        displayTasks();
        // console.log("Server response:", result);
    } catch (error) {
        // console.error("Error sending request:", error);
    }
}

async function createAndAddTaskToList(query, listId) {
    // console.log(`Sending AJAX request for: ${query}`);
    try {
        const response = await fetch(`/tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: query,
            }),
        })
        const result = await response.json();
        // console.log("Server response:", result);
        addTaskToList(query, listId);
    } catch (error) {
        // console.error("Error sending request:", error);
    }
}
displayTasks()
preloadData()