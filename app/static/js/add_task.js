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
            console.log(data);

            for (const task of data) {
                console.log(task);

                const taskElement = document.createElement("div");
                taskElement.classList.add("task");
                let isChecked = task.status ? "checked" : "";
                console.log(isChecked);

                taskElement.innerHTML = `
                <input type="checkbox" id="${task.name}" data-list-id="${listId}" class="taskCheckboxes " ${isChecked} onchange="return toggleTaskStatus(event) " />
                <label class="${isChecked ? "task-done" : ""}" for="task-${task.id}">${task.name}</label>`;
                tasksList.appendChild(taskElement);
            }
        });

        const toggleStatusBtn = document.querySelectorAll(".taskCheckboxes");
        for (const btn of toggleStatusBtn) {
            btn.addEventListener("change", (event) => {
                toggleTaskStatus(event);
                displayTasks()
            });
        }
    }
}

async function toggleTaskStatus(event) {
    const task = event.target.id;
    const listId = event.target.getAttribute("data-list-id");
    try {
        const response = await fetch(`/lists/${listId}/tasks/${task}/toggle_status`, {
            method: "POST",
        });
        const result = await response.json();
        displayTasks();
        // console.log("Server response:", result);
    } catch (error) {
        // console.error("Error sending request:", error);
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
        console.log(allData)
        let tasks_names = allData.map(task => task.name);

        const autoCompleteJS = new autoComplete({
            selector: selector,
            data: {
                src: tasks_names,
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