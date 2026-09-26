const API_BASE_URL = "http://127.0.0.1:8000";


// ======================================================
// DOM ELEMENTS
// ======================================================

// Register
const registerForm =
    document.querySelector(
        "#register-form"
    );

const registerEmailInput =
    document.querySelector(
        "#register-email"
    );

const registerPasswordInput =
    document.querySelector(
        "#register-password"
    );

const registerMessage =
    document.querySelector(
        "#register-message"
    );


// Login
const loginForm =
    document.querySelector(
        "#login-form"
    );

const loginEmailInput =
    document.querySelector(
        "#login-email"
    );

const loginPasswordInput =
    document.querySelector(
        "#login-password"
    );

const loginMessage =
    document.querySelector(
        "#login-message"
    );


// Views
const authView =
    document.querySelector(
        "#auth-view"
    );

const dashboardView =
    document.querySelector(
        "#dashboard-view"
    );

const currentUserEmail =
    document.querySelector(
        "#current-user-email"
    );


// Logout
const logoutButton =
    document.querySelector(
        "#logout-button"
    );


// Task form
const taskForm =
    document.querySelector(
        "#task-form"
    );

const taskTitleInput =
    document.querySelector(
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


// Task list
const tasksMessage =
    document.querySelector(
        "#tasks-message"
    );

const taskList =
    document.querySelector(
        "#task-list"
    );


// IMPORTANT:
// These must come AFTER registerForm,
// loginForm and taskForm are declared.

const registerButton =
    registerForm.querySelector(
        "button[type='submit']"
    );

const loginButton =
    loginForm.querySelector(
        "button[type='submit']"
    );

const taskSubmitButton =
    taskForm.querySelector(
        "button[type='submit']"
    );


// ======================================================
// UI HELPERS
// ======================================================

function setButtonLoading(
    button,
    isLoading,
    loadingText = "Loading..."
) {
    if (isLoading) {
        if (!button.disabled) {
            button.dataset.originalText =
                button.textContent;
        }

        button.disabled = true;

        button.textContent =
            loadingText;

        return;
    }


    button.disabled = false;

    button.textContent =
        button.dataset.originalText
        || button.textContent;
}


function showMessage(
    element,
    message,
    type
) {
    element.textContent =
        message;

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


function getErrorMessage(
    data,
    fallbackMessage
) {
    if (
        typeof data?.detail ===
        "string"
    ) {
        return data.detail;
    }


    if (
        Array.isArray(
            data?.detail
        )
    ) {
        const messages =
            data.detail.map(
                function (error) {
                    return error.msg;
                }
            );

        return messages.join(" ");
    }


    return fallbackMessage;
}


// ======================================================
// AUTHENTICATION HELPERS
// ======================================================

function getAccessToken() {
    return sessionStorage.getItem(
        "access_token"
    );
}


function showAuthView() {
    authView.classList.remove(
        "hidden"
    );

    dashboardView.classList.add(
        "hidden"
    );

    clearMessage(loginMessage);
}


function clearSession() {
    sessionStorage.removeItem(
        "access_token"
    );

    taskList.innerHTML = "";

    currentUserEmail.textContent = "";

    clearMessage(
        taskFormMessage
    );

    clearMessage(
        tasksMessage
    );

    showAuthView();
}


async function authenticatedFetch(
    endpoint,
    options = {}
) {
    const token =
        getAccessToken();


    if (!token) {
        clearSession();

        return null;
    }


    const headers = {
        ...options.headers,

        "Authorization":
            `Bearer ${token}`
    };


    const response =
        await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                ...options,
                headers
            }
        );


    if (
        response.status === 401 ||
        response.status === 403
    ) {
        clearSession();

        return null;
    }


    return response;
}


// ======================================================
// REGISTER
// ======================================================

async function handleRegister(event) {
    event.preventDefault();


    const email =
        registerEmailInput.value.trim();

    const password =
        registerPasswordInput.value;


    const userData = {
        email,
        password
    };


    clearMessage(
        registerMessage
    );


    setButtonLoading(
        registerButton,
        true,
        "Creating account..."
    );


    try {
        const response =
            await fetch(
                `${API_BASE_URL}/users/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        userData
                    )
                }
            );


        const data =
            await response.json();


        if (response.ok) {
            showMessage(
                registerMessage,
                "Account created successfully.",
                "success"
            );

            registerForm.reset();

            return;
        }


        if (
            response.status === 409
        ) {
            showMessage(
                registerMessage,
                getErrorMessage(
                    data,
                    "Email already registered."
                ),
                "error"
            );

            return;
        }


        if (
            response.status === 422
        ) {
            showMessage(
                registerMessage,
                getErrorMessage(
                    data,
                    "Please check the information you entered."
                ),
                "error"
            );

            return;
        }


        showMessage(
            registerMessage,
            getErrorMessage(
                data,
                "Registration failed."
            ),
            "error"
        );

    } catch (error) {
        console.error(error);

        showMessage(
            registerMessage,
            "Unable to connect to the server.",
            "error"
        );

    } finally {
        setButtonLoading(
            registerButton,
            false
        );
    }
}


// ======================================================
// LOGIN
// ======================================================

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


    clearMessage(
        loginMessage
    );


    setButtonLoading(
        loginButton,
        true,
        "Logging in..."
    );


    try {
        const response =
            await fetch(
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


        const data =
            await response.json();


        if (!response.ok) {
            showMessage(
                loginMessage,
                getErrorMessage(
                    data,
                    "Login failed."
                ),
                "error"
            );

            return;
        }


        sessionStorage.setItem(
            "access_token",
            data.access_token
        );


        const currentUser =
            await getCurrentUser();


        if (!currentUser) {
            showMessage(
                loginMessage,
                "Unable to verify login.",
                "error"
            );

            return;
        }


        loginForm.reset();


        await showDashboard(
            currentUser
        );

    } catch (error) {
        console.error(error);

        showMessage(
            loginMessage,
            "Unable to connect to the server.",
            "error"
        );

    } finally {
        setButtonLoading(
            loginButton,
            false
        );
    }
}


// ======================================================
// CURRENT USER
// ======================================================

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


// ======================================================
// DASHBOARD
// ======================================================

async function showDashboard(user) {
    authView.classList.add(
        "hidden"
    );

    dashboardView.classList.remove(
        "hidden"
    );


    currentUserEmail.textContent =
        user.email;


    const tasks =
        await getTasks();


    if (tasks) {
        renderTasks(tasks);
    }
}


function handleLogout() {
    clearSession();
}


// ======================================================
// GET TASKS
// ======================================================

async function getTasks() {
    clearMessage(
        tasksMessage
    );

    tasksMessage.textContent =
        "Loading tasks...";


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

        showMessage(
            tasksMessage,
            "Unable to load tasks.",
            "error"
        );

        return null;
    }
}


// ======================================================
// CREATE TASK
// ======================================================

async function handleCreateTask(
    event
) {
    event.preventDefault();


    const token =
        getAccessToken();


    if (!token) {
        clearSession();

        return;
    }


    const title =
        taskTitleInput.value.trim();

    const description =
        taskDescriptionInput.value.trim()
        || null;


    const taskData = {
        title,
        description,
        completed: false
    };


    clearMessage(
        taskFormMessage
    );


    setButtonLoading(
        taskSubmitButton,
        true,
        "Creating..."
    );


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


        if (!response) {
            return;
        }


        const data =
            await response.json();


        if (response.ok) {
            showMessage(
                taskFormMessage,
                "Task created successfully.",
                "success"
            );


            taskForm.reset();


            const tasks =
                await getTasks();


            if (tasks) {
                renderTasks(tasks);
            }


            return;
        }


        if (
            response.status === 422
        ) {
            showMessage(
                taskFormMessage,
                getErrorMessage(
                    data,
                    "Please check the task information."
                ),
                "error"
            );

            return;
        }


        showMessage(
            taskFormMessage,
            getErrorMessage(
                data,
                "Unable to create task."
            ),
            "error"
        );

    } catch (error) {
        console.error(error);

        showMessage(
            taskFormMessage,
            "Unable to create task.",
            "error"
        );

    } finally {
        setButtonLoading(
            taskSubmitButton,
            false
        );
    }
}


// ======================================================
// GENERIC PATCH TASK
// ======================================================

async function updateTask(
    taskId,
    updateData
) {
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
            return {
                success: false,
                data: null
            };
        }


        const data =
            await response.json();


        if (!response.ok) {
            return {
                success: false,
                data
            };
        }


        return {
            success: true,
            data
        };

    } catch (error) {
        console.error(error);

        return {
            success: false,
            data: null
        };
    }
}


// ======================================================
// DELETE TASK
// ======================================================

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


        if (
            response.status === 404
        ) {
            showMessage(
                tasksMessage,
                "Task not found.",
                "error"
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

        showMessage(
            tasksMessage,
            "Unable to delete task.",
            "error"
        );

        return false;
    }
}


// ======================================================
// TASK EDITOR
// ======================================================

function renderTaskEditor(
    task,
    taskElement
) {
    taskElement.innerHTML = "";


    const titleInput =
        document.createElement(
            "input"
        );

    titleInput.type = "text";

    titleInput.value =
        task.title;

    titleInput.maxLength = 200;

    titleInput.classList.add(
        "edit-title-input"
    );


    const descriptionInput =
        document.createElement(
            "textarea"
        );

    descriptionInput.value =
        task.description || "";

    descriptionInput.maxLength =
        1000;

    descriptionInput.rows = 4;

    descriptionInput.classList.add(
        "edit-description-input"
    );


    const editorMessage =
        document.createElement(
            "p"
        );

    editorMessage.classList.add(
        "form-message"
    );


    const saveButton =
        document.createElement(
            "button"
        );

    saveButton.type = "button";

    saveButton.textContent =
        "Save";

    saveButton.classList.add(
        "save-button"
    );


    const cancelButton =
        document.createElement(
            "button"
        );

    cancelButton.type = "button";

    cancelButton.textContent =
        "Cancel";

    cancelButton.classList.add(
        "cancel-button"
    );


    const editorActions =
        document.createElement(
            "div"
        );

    editorActions.classList.add(
        "editor-actions"
    );


    editorActions.appendChild(
        cancelButton
    );

    editorActions.appendChild(
        saveButton
    );


    taskElement.appendChild(
        titleInput
    );

    taskElement.appendChild(
        descriptionInput
    );

    taskElement.appendChild(
        editorMessage
    );

    taskElement.appendChild(
        editorActions
    );


    // ----------------------------------
    // Cancel editing
    // ----------------------------------

    cancelButton.addEventListener(
        "click",
        async function () {
            const tasks =
                await getTasks();


            if (tasks) {
                renderTasks(tasks);
            }
        }
    );


    // ----------------------------------
    // Save edited task
    // ----------------------------------

    saveButton.addEventListener(
        "click",
        async function () {
            clearMessage(
                editorMessage
            );


            const title =
                titleInput.value.trim();

            const description =
                descriptionInput
                    .value
                    .trim()
                || null;


            if (!title) {
                showMessage(
                    editorMessage,
                    "Title cannot be empty.",
                    "error"
                );

                return;
            }


            const updateData = {};


            // Only include title
            // if it actually changed.

            if (
                title !== task.title
            ) {
                updateData.title =
                    title;
            }


            const originalDescription =
                task.description || "";

            const newDescription =
                description || "";


            // Only include description
            // if it actually changed.

            if (
                newDescription !==
                originalDescription
            ) {
                updateData.description =
                    description;
            }


            // Nothing changed.
            // No PATCH request required.

            if (
                Object.keys(
                    updateData
                ).length === 0
            ) {
                const tasks =
                    await getTasks();


                if (tasks) {
                    renderTasks(
                        tasks
                    );
                }


                return;
            }


            setButtonLoading(
                saveButton,
                true,
                "Saving..."
            );

            cancelButton.disabled =
                true;


            const result =
                await updateTask(
                    task.id,
                    updateData
                );


            if (!result.success) {
                setButtonLoading(
                    saveButton,
                    false
                );

                cancelButton.disabled =
                    false;


                const message =
                    result.data
                        ? getErrorMessage(
                            result.data,
                            "Unable to update task."
                        )
                        : "Unable to update task.";


                showMessage(
                    editorMessage,
                    message,
                    "error"
                );


                return;
            }


            const tasks =
                await getTasks();


            if (tasks) {
                renderTasks(tasks);
            }
        }
    );


    titleInput.focus();
}


// ======================================================
// RENDER TASKS
// ======================================================

function renderTasks(tasks) {
    taskList.innerHTML = "";

    clearMessage(
        tasksMessage
    );


    if (tasks.length === 0) {
        tasksMessage.textContent =
            "You don't have any tasks yet.";

        return;
    }


    for (const task of tasks) {
        const taskElement =
            document.createElement(
                "div"
            );

        taskElement.classList.add(
            "task-item"
        );


        // ----------------------------------
        // Title
        // ----------------------------------

        const titleElement =
            document.createElement(
                "h3"
            );

        titleElement.textContent =
            task.title;


        // ----------------------------------
        // Description
        // ----------------------------------

        const descriptionElement =
            document.createElement(
                "p"
            );

        descriptionElement.textContent =
            task.description
            || "No description";


        // ----------------------------------
        // Status
        // ----------------------------------

        const statusContainer =
            document.createElement(
                "div"
            );

        statusContainer.classList.add(
            "task-status"
        );


        const checkbox =
            document.createElement(
                "input"
            );

        checkbox.type =
            "checkbox";

        checkbox.checked =
            task.completed;


        const statusLabel =
            document.createElement(
                "span"
            );

        statusLabel.textContent =
            task.completed
                ? "Completed"
                : "Pending";


        checkbox.addEventListener(
            "change",
            async function () {
                const newCompletedValue =
                    checkbox.checked;


                checkbox.disabled =
                    true;


                const result =
                    await updateTask(
                        task.id,
                        {
                            completed:
                                newCompletedValue
                        }
                    );


                if (result.success) {
                    checkbox.checked =
                        result.data.completed;

                    statusLabel.textContent =
                        result.data.completed
                            ? "Completed"
                            : "Pending";

                    checkbox.disabled =
                        false;

                    return;
                }


                // PATCH failed.
                // Restore previous value.

                checkbox.checked =
                    !newCompletedValue;

                checkbox.disabled =
                    false;


                // If authentication expired,
                // authenticatedFetch already
                // moved us to login.

                if (getAccessToken()) {
                    showMessage(
                        tasksMessage,
                        "Unable to update task.",
                        "error"
                    );
                }
            }
        );


        statusContainer.appendChild(
            checkbox
        );

        statusContainer.appendChild(
            statusLabel
        );


        // ----------------------------------
        // Edit button
        // ----------------------------------

        const editButton =
            document.createElement(
                "button"
            );

        editButton.type =
            "button";

        editButton.textContent =
            "Edit";

        editButton.classList.add(
            "edit-button"
        );


        editButton.addEventListener(
            "click",
            function () {
                renderTaskEditor(
                    task,
                    taskElement
                );
            }
        );


        // ----------------------------------
        // Delete button
        // ----------------------------------

        const deleteButton =
            document.createElement(
                "button"
            );

        deleteButton.type =
            "button";

        deleteButton.textContent =
            "Delete";

        deleteButton.classList.add(
            "delete-button"
        );


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


                setButtonLoading(
                    deleteButton,
                    true,
                    "Deleting..."
                );

                editButton.disabled =
                    true;

                checkbox.disabled =
                    true;


                const deleted =
                    await deleteTask(
                        task.id
                    );


                if (!deleted) {
                    setButtonLoading(
                        deleteButton,
                        false
                    );

                    editButton.disabled =
                        false;

                    checkbox.disabled =
                        false;

                    return;
                }


                const updatedTasks =
                    await getTasks();


                if (updatedTasks) {
                    renderTasks(
                        updatedTasks
                    );
                }
            }
        );


        // ----------------------------------
        // Actions
        // ----------------------------------

        const taskActions =
            document.createElement(
                "div"
            );

        taskActions.classList.add(
            "task-actions"
        );


        taskActions.appendChild(
            editButton
        );

        taskActions.appendChild(
            deleteButton
        );


        // ----------------------------------
        // Footer
        // ----------------------------------

        const taskFooter =
            document.createElement(
                "div"
            );

        taskFooter.classList.add(
            "task-footer"
        );


        taskFooter.appendChild(
            statusContainer
        );

        taskFooter.appendChild(
            taskActions
        );


        // ----------------------------------
        // Build card
        // ----------------------------------

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


// ======================================================
// EVENT LISTENERS
// ======================================================

registerForm.addEventListener(
    "submit",
    handleRegister
);


loginForm.addEventListener(
    "submit",
    handleLogin
);


logoutButton.addEventListener(
    "click",
    handleLogout
);


taskForm.addEventListener(
    "submit",
    handleCreateTask
);


// ======================================================
// APPLICATION INITIALIZATION
// ======================================================

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


initializeApp();