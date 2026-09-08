/* =========================================================
   CINE TIZA — DIRECTOR'S CUT
========================================================= */


// =========================================================
// ESTADO DEL JUGADOR
// =========================================================

const game = {

    nickname: "Director",

    title: "",

    genre: null,

    character: null,

    location: null,

    scene: 0,

    stats: {

        direction: 50,

        acting: 50,

        cinematography: 50,

        sound: 50,

        story: 50,

        creativity: 50,

        resources: 100

    }

};


// =========================================================
// DATOS
// =========================================================

const genres = [

    {
        id: "drama",
        name: "DRAMA",
        icon: "🎭",
        description: "Historias humanas",
        bonus: {
            acting: 8,
            story: 5
        },
        titles: [
            "La Última Mirada",
            "Lo Que Queda",
            "Antes de Irnos",
            "El Último Día"
        ]
    },

    {
        id: "comedy",
        name: "COMEDIA",
        icon: "😂",
        description: "Historias para reír",
        bonus: {
            creativity: 8,
            acting: 5
        },
        titles: [
            "El Plan Perfecto",
            "No Era Así",
            "Llegamos Tarde",
            "¿Quién Fue?"
        ]
    },

    {
        id: "horror",
        name: "TERROR",
        icon: "👻",
        description: "Historias que inquietan",
        bonus: {
            cinematography: 8,
            sound: 6
        },
        titles: [
            "La Última Puerta",
            "No Mires Atrás",
            "23:17",
            "La Casa Vacía"
        ]
    },

    {
        id: "scifi",
        name: "CIENCIA FICCIÓN",
        icon: "🚀",
        description: "Más allá de lo conocido",
        bonus: {
            creativity: 10,
            cinematography: 5
        },
        titles: [
            "Después del Mañana",
            "Código 07",
            "Señal Perdida",
            "Última Transmisión"
        ]
    },

    {
        id: "mystery",
        name: "MISTERIO",
        icon: "🔎",
        description: "Nada es lo que parece",
        bonus: {
            story: 8,
            direction: 5
        },
        titles: [
            "Después de las 23:00",
            "El Caso 17",
            "Sin Respuesta",
            "La Habitación"
        ]
    },

    {
        id: "experimental",
        name: "EXPERIMENTAL",
        icon: "🎨",
        description: "Romper las reglas",
        bonus: {
            creativity: 12,
            direction: 4
        },
        titles: [
            "Fragmentos",
            "Fuera de Cuadro",
            "Sin Nombre",
            "Entre Líneas"
        ]
    }

];


const characters = [

    {
        name: "EL ESTUDIANTE",
        icon: "🎒",
        description: "Autenticidad y espontaneidad",
        bonus: {
            acting: 7,
            creativity: 4
        }
    },

    {
        name: "EL DIRECTOR",
        icon: "🎥",
        description: "Control absoluto",
        bonus: {
            direction: 10
        }
    },

    {
        name: "EL MISTERIOSO",
        icon: "🕵️",
        description: "Una presencia difícil de entender",
        bonus: {
            story: 7,
            cinematography: 4
        }
    },

    {
        name: "EL VISITANTE",
        icon: "👽",
        description: "Algo completamente diferente",
        bonus: {
            creativity: 10
        }
    },

    {
        name: "EL AMIGO",
        icon: "🤡",
        description: "Energía y carisma",
        bonus: {
            acting: 8,
            creativity: 5
        }
    }

];


const locations = [

    {
        name: "LA ESCUELA",
        icon: "🏫",
        description: "El lugar donde todo comienza",
        bonus: {
            story: 7
        }
    },

    {
        name: "LA PLAZA",
        icon: "🌳",
        description: "Una locación abierta",
        bonus: {
            cinematography: 7
        }
    },

    {
        name: "LA CIUDAD",
        icon: "🏙️",
        description: "Movimiento constante",
        bonus: {
            direction: 5,
            cinematography: 5
        }
    },

    {
        name: "UNA CASA",
        icon: "🏠",
        description: "Un espacio íntimo",
        bonus: {
            acting: 6,
            sound: 4
        }
    },

    {
        name: "UN LUGAR ABANDONADO",
        icon: "🌙",
        description: "Perfecto para historias oscuras",
        bonus: {
            sound: 6,
            cinematography: 8
        }
    },

    {
        name: "UN ESTUDIO",
        icon: "🎬",
        description: "Todo bajo control",
        bonus: {
            direction: 8,
            cinematography: 5
        }
    }

];


// =========================================================
// EVENTOS DEL RODAJE
// =========================================================

const events = [

    {
        category: "PRODUCCIÓN",

        title: "EL ACTOR OLVIDÓ EL GUIÓN",

        description:
            "La cámara está lista. El equipo espera. Pero el protagonista no recuerda una sola línea.",

        choices: [

            {
                text: "Improvisar la escena.",
                effects: {
                    creativity: 8,
                    acting: 5,
                    story: -2
                }
            },

            {
                text: "Esperar hasta que memorice.",
                effects: {
                    acting: 7,
                    resources: -10
                }
            },

            {
                text: "Cambiar el guion.",
                effects: {
                    story: 6,
                    creativity: 5
                }
            },

            {
                text: "Grabar igual.",
                effects: {
                    acting: -5,
                    creativity: 4
                }
            }

        ]
    },


    {
        category: "SONIDO",

        title: "DEMASIADO RUIDO",

        description:
            "Justo cuando comienza la escena, aparece un ruido que arruina la grabación.",

        choices: [

            {
                text: "Regrabar.",
                effects: {
                    sound: 8,
                    resources: -12
                }
            },

            {
                text: "Continuar.",
                effects: {
                    sound: -8,
                    resources: 5
                }
            },

            {
                text: "Cambiar de ubicación.",
                effects: {
                    cinematography: 5,
                    sound: 7,
                    resources: -15
                }
            },

            {
                text: "Convertir el ruido en parte de la escena.",
                effects: {
                    creativity: 10,
                    sound: 3
                }
            }

        ]
    },


    {
        category: "PRODUCCIÓN",

        title: "QUEDA POCA BATERÍA",

        description:
            "La cámara marca 8%. Todavía falta grabar una escena importante.",

        choices: [

            {
                text: "Grabar inmediatamente.",
                effects: {
                    direction: 5,
                    resources: -5
                }
            },

            {
                text: "Buscar un cargador.",
                effects: {
                    resources: 10
                }
            },

            {
                text: "Reducir las tomas.",
                effects: {
                    direction: 5,
                    cinematography: -3
                }
            },

            {
                text: "Improvisar un final.",
                effects: {
                    creativity: 10,
                    story: 5,
                    resources: -5
                }
            }

        ]
    },


    {
        category: "CLIMA",

        title: "EMPIEZA A LLOVER",

        description:
            "Una lluvia inesperada comienza durante una escena exterior.",

        choices: [

            {
                text: "Suspender el rodaje.",
                effects: {
                    resources: -15,
                    cinematography: 2
                }
            },

            {
                text: "Incorporar la lluvia.",
                effects: {
                    cinematography: 10,
                    creativity: 7
                }
            },

            {
                text: "Cambiar el guion.",
                effects: {
                    story: 7,
                    creativity: 5
                }
            },

            {
                text: "Grabar rápidamente.",
                effects: {
                    direction: 6,
                    cinematography: 4,
                    sound: -5
                }
            }

        ]
    },


    {
        category: "ACTUACIÓN",

        title: "EL ACTOR QUIERE CAMBIAR LA ESCENA",

        description:
            "El protagonista propone una idea completamente diferente para la escena final.",

        choices: [

            {
                text: "Aceptar la idea.",
                effects: {
                    creativity: 10,
                    acting: 6
                }
            },

            {
                text: "Rechazarla.",
                effects: {
                    direction: 7,
                    creativity: -3
                }
            },

            {
                text: "Probar ambas versiones.",
                effects: {
                    acting: 5,
                    story: 5,
                    resources: -15
                }
            },

            {
                text: "Improvisar juntos.",
                effects: {
                    creativity: 8,
                    acting: 8
                }
            }

        ]
    },


    {
        category: "FOTOGRAFÍA",

        title: "LA LUZ NO ES LA IDEAL",

        description:
            "La escena está lista, pero la iluminación no acompaña la idea original.",

        choices: [

            {
                text: "Esperar la luz correcta.",
                effects: {
                    cinematography: 10,
                    resources: -12
                }
            },

            {
                text: "Usar la luz disponible.",
                effects: {
                    creativity: 7,
                    cinematography: 4
                }
            },

            {
                text: "Cambiar el encuadre.",
                effects: {
                    cinematography: 8,
                    direction: 4
                }
            },

            {
                text: "Hacerlo blanco y negro.",
                effects: {
                    creativity: 10,
                    cinematography: 5
                }
            }

        ]
    },


    {
        category: "FINAL",

        title: "LLEGÓ EL MOMENTO DEL FINAL",

        description:
            "Tenés una última oportunidad para cerrar tu película.",

        choices: [

            {
                text: "Un final emocional.",
                effects: {
                    story: 10,
                    acting: 6
                }
            },

            {
                text: "Un giro inesperado.",
                effects: {
                    story: 8,
                    creativity: 10
                }
            },

            {
                text: "Final abierto.",
                effects: {
                    creativity: 8,
                    cinematography: 6
                }
            },

            {
                text: "Final clásico.",
                effects: {
                    story: 6,
                    direction: 6
                }
            }

        ]
    }

];


// =========================================================
// ELEMENTOS
// =========================================================

const screens = document.querySelectorAll(".screen");

const genreContainer =
    document.getElementById("genreContainer");

const characterContainer =
    document.getElementById("characterContainer");

const locationContainer =
    document.getElementById("locationContainer");


// =========================================================
// CAMBIO DE PANTALLA
// =========================================================

function showScreen(id) {

    screens.forEach(screen => {

        screen.classList.remove("active");

    });

    document.getElementById(id).classList.add("active");
}


// =========================================================
// APLICAR EFECTOS
// =========================================================

function applyEffects(effects) {

    for (const stat in effects) {

        if (!game.stats.hasOwnProperty(stat)) continue;

        game.stats[stat] += effects[stat];

        game.stats[stat] =
            Math.max(
                0,
                Math.min(100, game.stats[stat])
            );
    }

    updateStats();
}


// =========================================================
// STATS
// =========================================================

function updateStats() {

    const stats = game.stats;

    const names = [
        "direction",
        "acting",
        "cinematography",
        "sound",
        "story",
        "creativity"
    ];

    names.forEach(name => {

        document.getElementById(
            `${name}Stat`
        ).textContent = Math.round(stats[name]);

        document.getElementById(
            `${name}Bar`
        ).style.width = `${stats[name]}%`;

    });

    document.getElementById("resourcesStat")
        .textContent = Math.round(stats.resources);
}


// =========================================================
// CREAR OPCIONES
// =========================================================

function createChoice(data, callback) {

    const button = document.createElement("button");

    button.className = "choice";

    button.innerHTML = `

        <span class="icon">
            ${data.icon}
        </span>

        <strong>
            ${data.name}
        </strong>

        <small>
            ${data.description}
        </small>

    `;

    button.addEventListener("click", callback);

    return button;
}


// =========================================================
// GÉNEROS
// =========================================================

genres.forEach(genre => {

    genreContainer.appendChild(

        createChoice(
            genre,
            () => {

                game.genre = genre;

                applyEffects(genre.bonus);

                updateProgress(50);

                showScreen("titleScreen");

            }
        )

    );

});


// =========================================================
// TÍTULO ALEATORIO
// =========================================================

document
    .getElementById("randomTitleBtn")
    .addEventListener("click", () => {

        const titleInput =
            document.getElementById("filmTitle");

        const titles =
            game.genre.titles;

        const random =
            titles[
            Math.floor(
                Math.random() * titles.length
            )
            ];

        titleInput.value = random;

    });


// =========================================================
// CONTINUAR TÍTULO
// =========================================================

document
    .getElementById("titleNextBtn")
    .addEventListener("click", () => {

        const input =
            document.getElementById("filmTitle");

        const title =
            input.value.trim();

        if (!title) {

            input.focus();

            return;
        }

        game.title = title;

        updateProgress(70);

        showScreen("characterScreen");

    });


// =========================================================
// PERSONAJES
// =========================================================

characters.forEach(character => {

    characterContainer.appendChild(

        createChoice(
            character,
            () => {

                game.character = character;

                applyEffects(character.bonus);

                updateProgress(85);

                showScreen("locationScreen");

            }
        )

    );

});


// =========================================================
// LOCACIONES
// =========================================================

locations.forEach(location => {

    locationContainer.appendChild(

        createChoice(
            location,
            () => {

                game.location = location;

                applyEffects(location.bonus);

                updateProgress(100);

                startShooting();

            }
        )

    );

});


// =========================================================
// PROGRESO
// =========================================================

function updateProgress(value) {

    document.getElementById(
        "progressBar"
    ).style.width = `${value}%`;

}


// =========================================================
// RODAJE
// =========================================================

let shuffledEvents = [];

function startShooting() {

    shuffledEvents =
        [...events]
            .sort(() => Math.random() - .5);

    game.scene = 0;

    updateStats();

    showScreen("shooting");

    showNextEvent();

}


// =========================================================
// SIGUIENTE EVENTO
// =========================================================

function showNextEvent() {

    if (
        game.scene >= shuffledEvents.length
    ) {

        finishGame();

        return;
    }

    const event =
        shuffledEvents[game.scene];

    document.getElementById(
        "sceneNumber"
    ).textContent =
        `SCENE ${String(game.scene + 1).padStart(2, "0")}`;

    document.getElementById(
        "eventCategory"
    ).textContent =
        event.category;

    document.getElementById(
        "eventTitle"
    ).textContent =
        event.title;

    document.getElementById(
        "eventDescription"
    ).textContent =
        event.description;


    const container =
        document.getElementById(
            "eventChoices"
        );

    container.innerHTML = "";


    event.choices.forEach(
        (choice, index) => {

            const button =
                document.createElement("button");

            button.className =
                "event-choice";

            button.textContent =
                `${String.fromCharCode(65 + index)}) ${choice.text}`;


            button.addEventListener(
                "click",
                () => {

                    applyEffects(
                        choice.effects
                    );

                    game.scene++;

                    setTimeout(
                        showNextEvent,
                        350
                    );

                }
            );


            container.appendChild(button);

        }
    );

}


// =========================================================
// FINALIZAR
// =========================================================

function finishGame() {

    const stats = game.stats;

    const score = Math.round(

        (
            stats.direction +
            stats.acting +
            stats.cinematography +
            stats.sound +
            stats.story +
            stats.creativity
        ) / 6

    );


    let category;
    let description;


    if (score >= 90) {

        category = "OBRA MAESTRA";

        description =
            "Una película extraordinaria. Tu mirada cinematográfica realmente destaca.";

    }
    else if (score >= 80) {

        category = "DIRECTOR DESTACADO";

        description =
            "Tenés una mirada cinematográfica muy definida. El público quiere ver más.";

    }
    else if (score >= 70) {

        category = "PROMESA DEL CINE";

        description =
            "Hay una gran historia detrás de tu película. Seguí filmando.";

    }
    else if (score >= 50) {

        category = "BUEN PRIMER CORTE";

        description =
            "La película sobrevivió al rodaje. Con algunas tomas más podría ser increíble.";

    }
    else {

        category = "CORTEN...";

        description =
            "El rodaje tuvo algunos problemas, pero toda gran película necesita otra toma.";

    }


    document.getElementById(
        "finalScore"
    ).textContent = score;


    document.getElementById(
        "finalCategory"
    ).textContent =
        game.genre.name;


    document.getElementById(
        "posterTitle"
    ).textContent =
        game.title;


    document.getElementById(
        "resultTitle"
    ).textContent =
        category;


    document.getElementById(
        "resultDescription"
    ).textContent =
        description;


    document.getElementById(
        "posterDirector"
    ).textContent =
        game.nickname.toUpperCase();


    document.getElementById(
        "finalDirection"
    ).textContent =
        Math.round(stats.direction);


    document.getElementById(
        "finalActing"
    ).textContent =
        Math.round(stats.acting);


    document.getElementById(
        "finalCinematography"
    ).textContent =
        Math.round(stats.cinematography);


    document.getElementById(
        "finalSound"
    ).textContent =
        Math.round(stats.sound);


    document.getElementById(
        "finalStory"
    ).textContent =
        Math.round(stats.story);


    document.getElementById(
        "finalCreativity"
    ).textContent =
        Math.round(stats.creativity);


    showScreen("result");

}


// =========================================================
// REINICIAR
// =========================================================

document
    .getElementById("restartBtn")
    .addEventListener("click", () => {

        location.reload();

    });


// =========================================================
// COMPARTIR
// =========================================================

document
    .getElementById("shareBtn")
    .addEventListener("click", async () => {

        const score =
            document.getElementById(
                "finalScore"
            ).textContent;

        const text =
            `🎬 Mi película "${game.title}" obtuvo ${score}/100 en Director's Cut de Cine Tiza. ¿Podés superarme?`;

        if (
            navigator.share
        ) {

            try {

                await navigator.share({
                    title: "Director's Cut — Cine Tiza",
                    text: text
                });

            } catch {

                // El usuario canceló compartir.

            }

        }
        else {

            await navigator.clipboard.writeText(text);

            alert(
                "¡Resultado copiado al portapapeles!"
            );

        }

    });


// =========================================================
// MODAL
// =========================================================

document
    .getElementById("howBtn")
    .addEventListener("click", () => {

        document
            .getElementById("howModal")
            .classList.add("active");

    });


document
    .getElementById("closeModal")
    .addEventListener("click", () => {

        document
            .getElementById("howModal")
            .classList.remove("active");

    });


// =========================================================
// COMENZAR
// =========================================================

document
    .getElementById("startBtn")
    .addEventListener("click", () => {

        showScreen("creation");

    });


// =========================================================
// TECLA ESC PARA CERRAR MODAL
// =========================================================

document.addEventListener(
    "keydown",
    event => {

        if (event.key === "Escape") {

            document
                .getElementById("howModal")
                .classList.remove("active");

        }

    }
);