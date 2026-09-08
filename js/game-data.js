/**
 * CINE TIZA — Director's Cut
 * game-data.js — Contenido del juego (escenas, géneros, personajes, locaciones)
 * Separado del motor para agregar contenido fácilmente sin tocar la lógica.
 */

const GAME_DATA = {

  /* ─────────────────────────── GÉNEROS ─────────────────────────── */
  genres: [
    { id: 'DRAMA',           emoji: '🎭', label: 'Drama',           color: '#8B5CF6' },
    { id: 'COMEDIA',         emoji: '😂', label: 'Comedia',         color: '#10B981' },
    { id: 'TERROR',          emoji: '👻', label: 'Terror',          color: '#EF4444' },
    { id: 'CIENCIA_FICCION', emoji: '🚀', label: 'Ciencia Ficción', color: '#3B82F6' },
    { id: 'MISTERIO',        emoji: '🔎', label: 'Misterio',        color: '#F59E0B' },
    { id: 'EXPERIMENTAL',    emoji: '🎨', label: 'Experimental',    color: '#EC4899' },
  ],

  /* ─────────────────────────── PERSONAJES ─────────────────────────── */
  characters: [
    { id: 'ESTUDIANTE', emoji: '🎒', label: 'El Estudiante',  bonus: { acting: 5, story: 3 },         bonusLabel: '+5 Autenticidad' },
    { id: 'DIRECTOR',   emoji: '🎥', label: 'El Director',    bonus: { direction: 5, creativity: 3 },  bonusLabel: '+5 Dirección' },
    { id: 'MISTERIOSO', emoji: '🕵️', label: 'El Misterioso',  bonus: { story: 5, cinematography: 3 }, bonusLabel: '+5 Tensión' },
    { id: 'VISITANTE',  emoji: '👽', label: 'El Visitante',   bonus: { creativity: 5, acting: 3 },    bonusLabel: '+5 Creatividad' },
    { id: 'AMIGO',      emoji: '🤡', label: 'El Amigo',       bonus: { acting: 5, direction: 3 },     bonusLabel: '+5 Conexión' },
  ],

  /* ─────────────────────────── LOCACIONES ─────────────────────────── */
  locations: [
    { id: 'ESCUELA',    emoji: '🏫', label: 'La Escuela',         mod: { acting: 5 } },
    { id: 'PLAZA',      emoji: '🌳', label: 'La Plaza',           mod: { cinematography: 5 } },
    { id: 'CIUDAD',     emoji: '🏙️', label: 'La Ciudad',          mod: { story: 5 } },
    { id: 'CASA',       emoji: '🏠', label: 'Una Casa',           mod: { sound: 5 } },
    { id: 'ABANDONADO', emoji: '🌙', label: 'Lugar Abandonado',   mod: { creativity: 5 } },
    { id: 'ESTUDIO',    emoji: '🎬', label: 'Un Estudio',         mod: { direction: 5 } },
  ],

  /* ─────────────────────────── TÍTULOS ALEATORIOS ─────────────────────────── */
  randomTitles: {
    DRAMA:           ['El Último Ensayo', 'Algo Que Decir', 'La Decisión', 'Voces del Pasillo', 'Sin Red'],
    COMEDIA:         ['El Plan Perfecto', 'Todo Mal', 'La Obra de Teatro', 'El Ensayo Final', 'Caos Organizado'],
    TERROR:          ['La Última Puerta', 'No Entres', 'El Pasillo de Noche', 'Quedarse', 'El Turno de Guardia'],
    CIENCIA_FICCION: ['El Protocolo', 'Señal Perdida', 'Sistema 07', 'La Prueba', 'Año Cero'],
    MISTERIO:        ['Después de las 23:00', 'El Cuarto Piso', 'La Clave', 'Quién Sabe', 'Rastros'],
    EXPERIMENTAL:    ['Sin Título', 'Frame 001', 'Estática', 'Movimiento', 'El Grano'],
  },

  /* ─────────────────────────── ESCENAS (7) ─────────────────────────── */
  scenes: [
    {
      id: 'scene_01',
      sceneNum: 1,
      icon: '🎬',
      title: 'El actor olvidó el guion',
      description: 'La cámara está lista, el equipo en posición, pero el actor principal blanqueó. Son las 9 de la mañana y ya se perdió media hora de rodaje.',
      choices: [
        { letter: 'A', text: 'Improvisar — que salga lo que salga.',     effects: { acting: 8, story: -5, creativity: 6 } },
        { letter: 'B', text: 'Esperar 20 minutos para que lo memorice.', effects: { acting: 12, story: 8 } },
        { letter: 'C', text: 'Reescribir la escena sobre la marcha.',    effects: { story: 6, creativity: 4 } },
        { letter: 'D', text: 'Grabar igual con el guion en mano.',       effects: { acting: -8, cinematography: 4 } },
      ]
    },
    {
      id: 'scene_02',
      sceneNum: 2,
      icon: '🎙️',
      title: 'Ruido en el rodaje',
      description: 'El micro capta todo: una cortadora de pasto, un perro, una alarma de auto. El ambiente sonoro es un desastre.',
      choices: [
        { letter: 'A', text: 'Regrabar cuando haya silencio.',                   effects: { sound: 12, resources: -5 } },
        { letter: 'B', text: 'Grabar igual y arreglar en post.',                 effects: { sound: -10, cinematography: 2 } },
        { letter: 'C', text: 'Cambiar a una locación interior.',                 effects: { resources: -8, creativity: 4 } },
        { letter: 'D', text: 'Incorporar el sonido como parte de la escena.',    effects: { sound: 6, creativity: 10, story: 4 } },
      ]
    },
    {
      id: 'scene_03',
      sceneNum: 3,
      icon: '🔋',
      title: 'Batería al 8%',
      description: 'La cámara principal está a punto de apagarse y nadie trajo el cargador. Quedan tres escenas por filmar.',
      choices: [
        { letter: 'A', text: 'Grabar la escena más importante ahora.',         effects: { cinematography: 10, resources: -12 } },
        { letter: 'B', text: 'Ir a buscar un cargador.',                       effects: { resources: -5 } },
        { letter: 'C', text: 'Reducir las tomas al mínimo.',                   effects: { cinematography: 5, resources: -3 } },
        { letter: 'D', text: 'Improvisar un final con lo que tenemos.',        effects: { creativity: 8, story: 6, resources: -8 } },
      ]
    },
    {
      id: 'scene_04',
      sceneNum: 4,
      icon: '🌧️',
      title: 'Empieza a llover',
      description: 'Sin pronóstico, sin paraguas. La lluvia arrasa con la locación exterior donde estaban filmando la escena central.',
      choices: [
        { letter: 'A', text: 'Suspender y reprogramar.',                         effects: { resources: -5, acting: 3 } },
        { letter: 'B', text: 'Incorporar la lluvia — es perfecto para el clima.', effects: { cinematography: 12, story: 8, creativity: 6 } },
        { letter: 'C', text: 'Cambiar el guion para una escena interior.',        effects: { story: 5, creativity: 3 } },
        { letter: 'D', text: 'Grabar rápido antes de que empeore.',              effects: { acting: 8, cinematography: 6, resources: -10 } },
      ]
    },
    {
      id: 'scene_05',
      sceneNum: 5,
      icon: '🎭',
      title: 'El actor quiere cambiar la escena',
      description: 'El protagonista interrumpe: "¿No sería mejor si en vez de esto, hacemos algo completamente diferente?" Tiene una idea. Puede ser brillante o un desastre.',
      choices: [
        { letter: 'A', text: 'Escucharlo y probar su idea.',                effects: { acting: 10, story: 8, creativity: 4 } },
        { letter: 'B', text: 'Seguir el guion original.',                    effects: { direction: 8, story: 3 } },
        { letter: 'C', text: 'Filmar ambas versiones.',                      effects: { creativity: 10, direction: 4, resources: -5 } },
        { letter: 'D', text: 'Mezclar su idea con la tuya.',                 effects: { acting: 6, creativity: 8, story: 4 } },
      ]
    },
    {
      id: 'scene_06',
      sceneNum: 6,
      icon: '😷',
      title: 'El camarógrafo se enfermó',
      description: 'Es la escena más técnica del corto y el camarógrafo no puede venir. Quedan 2 horas de luz natural.',
      choices: [
        { letter: 'A', text: 'Asumir la cámara vos mismo.',                      effects: { direction: 10, cinematography: 8 } },
        { letter: 'B', text: 'Contratar a alguien de urgencia.',                  effects: { resources: -10, cinematography: 12 } },
        { letter: 'C', text: 'Filmar con el celular — puro guerrilla.',           effects: { cinematography: -5, creativity: 8 } },
        { letter: 'D', text: 'Repensar la escena para que no necesite cámara fija.', effects: { story: 8, creativity: 10, cinematography: -5 } },
      ]
    },
    {
      id: 'scene_07',
      sceneNum: 7,
      icon: '😤',
      title: 'Tensión en el set',
      description: 'Dos miembros del equipo entraron en conflicto. El clima se cortó con machete. La última escena del día sigue sin filmarse.',
      choices: [
        { letter: 'A', text: 'Tomar el control y dar órdenes claras.',            effects: { direction: 12, acting: -5 } },
        { letter: 'B', text: 'Escuchar a ambas partes y mediar.',                 effects: { acting: 8, direction: 4, creativity: 4 } },
        { letter: 'C', text: 'Hacer un descanso y retomar en frío.',              effects: { resources: -8, acting: 5, direction: 5 } },
        { letter: 'D', text: 'Canalizar la tensión dentro de la actuación.',     effects: { creativity: 12, story: 8, acting: 6 } },
      ]
    },
  ],

  /* ─────────────────────────── RESULTADOS ─────────────────────────── */
  scoreCategories: [
    { min: 90, emoji: '🏆', label: 'OBRA MAESTRA',       desc: 'El festival necesita conocer tu película.' },
    { min: 80, emoji: '🎬', label: 'DIRECTOR DESTACADO', desc: 'Tenés una mirada cinematográfica clara.' },
    { min: 70, emoji: '⭐', label: 'PROMESA DEL CINE',   desc: 'Hay algo muy interesante acá.' },
    { min: 50, emoji: '🎥', label: 'BUEN PRIMER CORTE',  desc: 'La película sobrevivió al rodaje. No es poco.' },
    { min:  0, emoji: '🎞️', label: 'CORTEN...',          desc: 'Quizás la próxima toma salga mejor. Seguí.' },
  ],

  /* ─────────────────────────── PÓSTER COLORES POR GÉNERO ─────────────────────────── */
  posterPalettes: {
    DRAMA:           { bg: ['#1a0e2e', '#2d1b69'], accent: '#9D4EDD', text: '#F5F3EE' },
    COMEDIA:         { bg: ['#0f2027', '#203a43'], accent: '#10B981', text: '#F5F3EE' },
    TERROR:          { bg: ['#1a0000', '#3d0000'], accent: '#D93636', text: '#F5F3EE' },
    CIENCIA_FICCION: { bg: ['#0a0e2a', '#1a2060'], accent: '#3A86FF', text: '#F5F3EE' },
    MISTERIO:        { bg: ['#1a1200', '#3d2e00'], accent: '#FFD447', text: '#F5F3EE' },
    EXPERIMENTAL:    { bg: ['#1a0014', '#3d002f'], accent: '#EC4899', text: '#F5F3EE' },
  },
};
