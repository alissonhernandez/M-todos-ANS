const btn_cantidad_puntos = document.getElementById('btn-cantidad-puntos');


btn_cantidad_puntos.addEventListener('click', (e) => {
    e.preventDefault();
    const cantidad_puntos = parseInt(document.getElementById('cantidad-puntos').value);
    if (cantidad_puntos == 0 || isNaN(cantidad_puntos)) {
        alert('Por favor ingrese un número válido de puntos');
        return;
    }

    // Validación de la cantidad de puntos
    if (cantidad_puntos < 2) {
        alert('La cantidad de puntos debe ser mayor o igual a 2');
        return;
    }

    // Creación de los campos de los puntos
    const puntos = document.getElementById('puntos');

    // Verifica si ya existen campos de puntos para eliminarlos
    if (puntos.children.length == 2) {
        const p = document.getElementById('p-instrucciones');
        p.textContent = "Ingrese la información solicitada para cada Xi, f(Xi) y f'(Xi)";

        const input_cantidad_puntos = document.createElement('input');
        input_cantidad_puntos.type = 'number';
        input_cantidad_puntos.name = 'cantidad_puntos';
        input_cantidad_puntos.id = 'cantidad_puntos';
        input_cantidad_puntos.value = cantidad_puntos;
        input_cantidad_puntos.hidden = true;
        puntos.appendChild(input_cantidad_puntos);

        for (let i = 0; i < cantidad_puntos; i++) {
            const div = document.createElement('div');
            div.classList.add('form-group');
            div.innerHTML = `
                <label for="x-${i}">X(${i}) =></label>
                <input type="number" class="form-control" id="x-${i}" name="x-${i}" step="any" required>
                <label for="fx-${i}">f(X${i}) =></label>
                <input type="number" step="any" class="form-control" step="any" id="fx-${i}" name="fx-${i}" step="any" required>
                <label for="fdx-${i}">f'(X${i}) =></label>
                <input type="number" step="any" class="form-control" v id="fdx-${i}" name="fdx-${i}" step="any" required>
            `;
            puntos.appendChild(div);
        }
        const btn_calc_hermite = document.createElement('input');
        btn_calc_hermite.type = 'submit';
        btn_calc_hermite.id = 'calc-hermite';
        btn_calc_hermite.value = 'Resolver';
        puntos.appendChild(btn_calc_hermite);
    } else {
        alert('Ya se han creado los campos de puntos, por favor recargue la página para volver a ingresar la cantidad de puntos');
    }
});