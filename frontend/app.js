const API_BASE_URL = "http://127.0.0.1:8000";

const registerForm = document.querySelector(
    "#register-form"
);

const registerEmailInput = document.querySelector(
    "#register-email"
);

const registerPasswordInput = document.querySelector(
    "#register-password"
);

const registerMessage = document.querySelector(
    "#register-message"
);

const loginForm = document.querySelector(
    "#login-form"
);

const loginEmailInput = document.querySelector(
    "#login-email"
);

const loginPasswordInput = document.querySelector(
    "#login-password"
);

const loginMessage = document.querySelector(
    "#login-message"
);

const authView = document.querySelector(
    "#auth-view"
);

const dashboardView = document.querySelector(
    "#dashboard-view"
);

const currentUserEmail =
    document.querySelector(
        "#current-user-email"
    );

const logoutButton = document.querySelector(
    "#logout-button"
);

const taskForm = document.querySelector(
    "#task-form"
);

const taskTitleInput = document.querySelector(
    "#task-title"
);

const taskDescriptionInput =
    document.querySelector(
        "#task-description"
    );

const taskFormMessage =
    document.querySelector(
        "#task-form-message"
    );

const tasksMessage = document.querySelector(
    "#tasks-message"
);

const taskList = document.querySelector(
    "#task-list"
);

function showAuthView() {
    authView.classList.remove(
        "hidden"
    );

    dashboardView.classList.add(
        "hidden"
    );
    loginMessage.textContent = "";
}

function clearSession() {
    sessionStorage.removeItem(
        "access_token"
    );

    showAuthView();
}

function getAccessToken() {
    return sessionStorage.getItem(
        "access_token"
    );
}

function showMessage(
    element,
    message,
    type
) {
    element.textContent = message;

    element.classList.remove(
        "message-success",
        "message-error"
    );


    if (type === "success") {
        element.classList.add(
            "message-success"
        );
    }


    if (type === "error") {
        element.classList.add(
            "message-error"
        );
    }
}

function clearMessage(element) {
    element.textContent = "";

    element.classList.remove(
        "message-success",
        "message-error"
    );
}

async function authenticatedFetch(
    endpoint,
    options = {}
) {
    const token = getAccessToken();

    if (!token) {
        clearSession();

        return null;
    }


    const headers = {
        ...options.headers,

        "Authorization":
            `Bearer ${token}`
    };


    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,
            headers
        }
    );


    if (response.status === 401) {
        clearSession();

        return null;
    }

    return response;
}

async function showDashboard(user) {
    authView.classList.add(
        "hidden"
    );

    dashboardView.classList.remove(
        "hidden"
    );

    currentUserEmail.textContent =
        user.email;

    const tasks = await getTasks();

    if (tasks) {
        renderTasks(tasks);
    }
}

async function initializeApp() {
    const currentUser =
        await getCurrentUser();

    if (currentUser) {
        await showDashboard(
            currentUser
        );

        return;
    }

    showAuthView();
}

async function handleRegister(event) {
    event.preventDefault();

    const email = registerEmailInput.value.trim();
    const password = registerPasswordInput.value;

    const userData = {
        email,
        password
    };

    try {
        const response = await fetch(
            `${API_BASE_URL}/users/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(userData)
            }
        );

        const data = await response.json();


        if (response.ok) {
            registerMessage.textContent =
                "Account created successfully.";

            registerMessage.classList.remove(
                "message-error"
            );

            registerMessage.classList.add(
                "message-success"
            );

            registerForm.reset();

            return;
        }


        if (response.status === 409) {
            registerMessage.textContent =
                data.detail;

            registerMessage.classList.remove(
                "message-success"
            );

            registerMessage.classList.add(
                "message-error"
            );

            return;
        }


        if (response.status === 422) {
            registerMessage.textContent =
                "Please check the information you entered.";

            registerMessage.classList.remove(
                "message-success"
            );

            registerMessage.classList.add(
                "message-error"
            );

            return;
        }


        registerMessage.textContent =
            data.detail || "Registration failed.";

        registerMessage.classList.remove(
            "message-success"
        );

        registerMessage.classList.add(
            "message-error"
        );

    } catch (error) {
        registerMessage.textContent =
            "Unable to connect to the server.";

        registerMessage.classList.remove(
            "message-success"
        );

        registerMessage.classList.add(
            "message-error"
        );

        console.error(error);
    }
}


registerForm.addEventListener(
    "submit",
    handleRegister
);


async function getCurrentUser() {
    if (!getAccessToken()) {
        return null;
    }


    try {
        const response =
            await authenticatedFetch(
                "/users/me"
            );


        if (!response) {
            return null;
        }


        if (!response.ok) {
            return null;
        }


        return await response.json();

    } catch (error) {
        console.error(error);

        return null;
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const email =
        loginEmailInput.value.trim();

    const password =
        loginPasswordInput.value;

    const credentials = {
        email,
        password
    };

    try {
        const response = await fetch(
            `${API_BASE_URL}/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    credentials
                )
            }
        );

        const data = await response.json();


        if (response.ok) {
            sessionStorage.setItem(
                "access_token",
                data.access_token
            );

            const currentUser = await getCurrentUser();
            if (currentUser) {
                await showDashboard(currentUser);}

            showMessage(loginMessage,"Login successful", "success");

            loginForm.reset();

            return;
        }


        if (response.status === 401) {
            loginMessage.textContent =
                data.detail;

            loginMessage.classList.remove(
                "message-success"
            );

            loginMessage.classList.add(
                "message-error"
            );

            return;
        }


        loginMessage.textContent =
            data.detail || "Login failed.";

        loginMessage.classList.remove(
            "message-success"
        );

        loginMessage.classList.add(
            "message-error"
        );

    } catch (error) {
        loginMessage.textContent =
            "Unable to connect to the server.";

        loginMessage.classList.remove(
            "message-success"
        );

        loginMessage.classList.add(
            "message-error"
        );

        console.error(error);
    }
}

function handleLogout() {
    clearSession();
}

loginForm.addEventListener(
    "submit",
    handleLogin
);

logoutButton.addEventListener(
    "click",
    handleLogout
);

async function getTasks() {
    try {
        const response =
            await authenticatedFetch(
                "/tasks"
            );

        if (!response) {
            return null;
        }


        if (!response.ok) {
            throw new Error(
                "Failed to load tasks"
            );
        }


        return await response.json();

    } catch (error) {
        console.error(error);

        tasksMessage.textContent =
            "Unable to load tasks.";

        tasksMessage.classList.add(
            "message-error"
        );

        return null;
    }
}

function renderTasks(tasks) {
    taskList.innerHTML = "";
    clearMessage(tasksMessage);

    if (tasks.length === 0) {
        tasksMessage.textContent =
            "You don't have any tasks yet.";

        return;
    }


    for (const task of tasks) {
        const taskElement =
            document.createElement("div");

        taskElement.classList.add(
            "task-item"
        );


        const titleElement =
            document.createElement("h3");

        titleElement.textContent =
            task.title;


        const descriptionElement =
            document.createElement("p");

        descriptionElement.textContent =
            task.description ||
            "No description";


        const statusContainer =
            document.createElement("div");

        statusContainer.classList.add(
            "task-status"
        );


        const checkbox =
            document.createElement("input");

        checkbox.type = "checkbox";

        checkbox.checked =
            task.completed;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.classList.add("delete-button");

        deleteButton.addEventListener(
    "click",
    async function () {
        const shouldDelete =
            confirm(
                `Delete "${task.title}"?`
            );

        if (!shouldDelete) {
            return;
        }


        const deleted =
            await deleteTask(task.id);

        if (!deleted) {
            return;
        }


        const tasks =
            await getTasks();

        if (tasks) {
            renderTasks(tasks);
        }
    });

        const taskFooter = document.createElement("div");
        taskFooter.classList.add("task-footer");

        taskFooter.appendChild(statusContainer);
        taskFooter.appendChild(deleteButton);

        checkbox.addEventListener("change",
           async function () {
            const newCompletedValue = checkbox.checked;

            const updatedTask = await updateTaskStatus(task.id, newCompletedValue);


            if (updatedTask) {
            statusLabel.textContent =
                updatedTask.completed
                    ? "Completed"
                    : "Pending";

            return;
        }


        checkbox.checked =
            !newCompletedValue;
    });


        const statusLabel =
            document.createElement("span");

        statusLabel.textContent =
            task.completed
                ? "Completed"
                : "Pending";


        statusContainer.appendChild(
            checkbox
        );

        statusContainer.appendChild(
            statusLabel
        );


        taskElement.appendChild(
            titleElement
        );

        taskElement.appendChild(
            descriptionElement
        );

        taskElement.appendChild(
            taskFooter
        );


        taskList.appendChild(
            taskElement
        );
    }
}

async function handleCreateTask(event) {
    event.preventDefault();

    const title =
        taskTitleInput.value.trim();

    const description =
        taskDescriptionInput.value.trim()
        || null;

    const token = getAccessToken();

    if (!token) {
        showAuthView();

        return;
    }

    const taskData = {
        title,
        description,
        completed: false
    };

    try {
        const response =
    await authenticatedFetch(
        "/tasks",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(
                taskData
            )
        }
    );

        const data = await response.json();


        if (response.ok) {
            showMessage(taskFormMessage,"Task created successfully.", "success");

            taskForm.reset();


            const tasks = await getTasks();

            if (tasks) {
                renderTasks(tasks);
            }

            return;
        }

        if (response.status === 422) {
            taskFormMessage.textContent =
                "Please check the task information.";

            taskFormMessage.classList.remove(
                "message-success"
            );

            taskFormMessage.classList.add(
                "message-error"
            );
            showMessage(taskFormMessage,"Please check the task information.", "error");

            return;
        }


        taskFormMessage.textContent =
            data.detail ||
            "Unable to create task.";

        taskFormMessage.classList.remove(
            "message-success"
        );

        taskFormMessage.classList.add(
            "message-error"
        );

    } catch (error) {
        taskFormMessage.textContent =
            "Unable to create task.";

        taskFormMessage.classList.remove(
            "message-success"
        );

        taskFormMessage.classList.add(
            "message-error"
        );

        console.error(error);
    }
}

taskForm.addEventListener(
    "submit",
    handleCreateTask
);

async function updateTaskStatus(
    taskId,
    completed
) {
    const updateData = {
        completed
    };


    try {
        const response =
            await authenticatedFetch(
                `/tasks/${taskId}`,
                {
                    method: "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        updateData
                    )
                }
            );


        if (!response) {
            return null;
        }


        if (response.status === 404) {
            tasksMessage.textContent =
                "Task not found.";

            tasksMessage.classList.add(
                "message-error"
            );

            return null;
        }


        if (!response.ok) {
            throw new Error(
                "Failed to update task"
            );
        }


        return await response.json();

    } catch (error) {
        console.error(error);

        tasksMessage.textContent =
            "Unable to update task.";

        tasksMessage.classList.add(
            "message-error"
        );

        return null;
    }
}

async function deleteTask(taskId) {
    try {
        const response =
            await authenticatedFetch(
                `/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response) {
            return false;
        }


        if (response.status === 404) {
            tasksMessage.textContent =
                "Task not found.";

            tasksMessage.classList.add(
                "message-error"
            );

            return false;
        }


        if (!response.ok) {
            throw new Error(
                "Failed to delete task"
            );
        }


        return true;

    } catch (error) {
        console.error(error);

        tasksMessage.textContent =
            "Unable to delete task.";

        tasksMessage.classList.add(
            "message-error"
        );

        return false;
    }
}

initializeApp();