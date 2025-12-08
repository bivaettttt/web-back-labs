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

                const tdTitleRu = document.createElement('td');
                const tdTitle = document.createElement('td');
                const tdYear = document.createElement('td');
                const tdActions = document.createElement('td');

                tdTitleRu.textContent = film.title_ru;

                if (film.title === film.title_ru) {
                    tdTitle.textContent = '';
                } else {
                    tdTitle.textContent = film.title;
                }

                tdYear.textContent = film.year;

                const editButton = document.createElement('button');
                editButton.textContent = 'Редактировать';
                // обработчик редактирования будет в пункте 11

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Удалить';
                deleteButton.onclick = function () {
                    deleteFilm(i, film.title_ru);
                };

                tdActions.appendChild(editButton);
                tdActions.appendChild(deleteButton);

                tr.appendChild(tdTitleRu);
                tr.appendChild(tdTitle);
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

/* ----- модальное окно для добавления фильма (п.10) ----- */

function showModal() {
    clearModal();
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

    fetch('/lab7/rest-api/films/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    }).then(function () {
        hideModal();
        fillFilmList();
    });
}
