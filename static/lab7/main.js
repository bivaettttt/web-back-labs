let editingFilmId = null;

function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function(response) {
            return response.json();
        })
        .then(function(films) {
            const tbody = document.getElementById('film-table-body');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                const film = films[i];

                const tr = document.createElement('tr');

                const tdTitleOriginal = document.createElement('td');
                const tdTitleRu = document.createElement('td');
                const tdYear = document.createElement('td');
                const tdActions = document.createElement('td');

                if (film.title && film.title !== film.title_ru) {
                    tdTitleOriginal.innerHTML =
                        '<span class="original-title">(' +
                        film.title +
                        ')</span>';
                } else {
                    tdTitleOriginal.textContent = '';
                }

                tdTitleRu.textContent = film.title_ru;
                tdYear.textContent = film.year;

                const editButton = document.createElement('button');
                editButton.textContent = 'Редактировать';
                editButton.onclick = function () {
                    editFilm(i);
                };

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Удалить';
                deleteButton.onclick = function () {
                    deleteFilm(i, film.title_ru);
                };

                tdActions.appendChild(editButton);
                tdActions.appendChild(deleteButton);

                tr.appendChild(tdTitleOriginal);
                tr.appendChild(tdTitleRu);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);

                tbody.appendChild(tr);
            }
        });
}

function deleteFilm(id, titleRu) {
    let message = 'Удалить этот фильм?';
    if (titleRu) {
        message = 'Удалить фильм "' + titleRu + '"?';
    }

    if (!confirm(message)) {
        return;
    }

    fetch('/lab7/rest-api/films/' + id, {
        method: 'DELETE'
    }).then(function () {
        fillFilmList();
    });
}

function showModal() {
    editingFilmId = null;
    clearModal();
    clearErrorMessage();

    const modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function hideModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function clearModal() {
    document.getElementById('film-title-ru').value = '';
    document.getElementById('film-title').value = '';
    document.getElementById('film-year').value = '';
    document.getElementById('film-description').value = '';
}

function clearErrorMessage() {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = '';
        errorDiv.style.display = 'none';
    }
}

function editFilm(id) {
    fetch('/lab7/rest-api/films/' + id)
        .then(function(response) {
            return response.json();
        })
        .then(function(film) {
            document.getElementById('film-title-ru').value = film.title_ru;
            document.getElementById('film-title').value = film.title;
            document.getElementById('film-year').value = film.year;
            document.getElementById('film-description').value = film.description || '';

            editingFilmId = id;
            clearErrorMessage();

            const modal = document.querySelector('.modal');
            if (modal) {
                modal.style.display = 'flex';
            }
        });
}

function sendFilm() {
    const titleRu = document.getElementById('film-title-ru').value;
    let title = document.getElementById('film-title').value;
    const yearValue = document.getElementById('film-year').value;
    const description = document.getElementById('film-description').value;

    if (!title) {
        title = titleRu;
    }

    const year = parseInt(yearValue);

    const film = {
        title: title,
        title_ru: titleRu,
        year: year,
        description: description
    };

    let url;
    let method;

    if (editingFilmId === null) {
        url = '/lab7/rest-api/films/';
        method = 'POST';
    } else {
        url = '/lab7/rest-api/films/' + editingFilmId;
        method = 'PUT';
    }

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(function(response) {
        if (response.ok) {
            return {};
        }
        return response.json();
    })
    .then(function(data) {
        if (data.description) {
            const errorDiv = document.getElementById('error-message');
            if (errorDiv) {
                errorDiv.textContent = data.description;
                errorDiv.style.display = 'block';
            }
        } else {
            clearErrorMessage();
            hideModal();
            fillFilmList();
        }
    });
}