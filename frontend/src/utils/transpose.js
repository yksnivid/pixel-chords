function escapeChords(text) {
  // Регулярное выражение для поиска аккордов без экранирования
  const chordRegex = /\b([A-G][#b]?(?:m|maj|aug|dim|sus)?(?:6|7|9|11|13)?(?:\/[A-G][#b]?)?)\b/g;

  // Заменяем найденные аккорды на [аккорд]
  return text.replace(chordRegex, '[$1]');
}

export { escapeChords };
