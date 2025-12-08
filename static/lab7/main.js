function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
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

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Удалить';

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