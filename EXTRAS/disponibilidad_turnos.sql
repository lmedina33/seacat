SELECT date.id, date.date, date.type, count(turn.uid) FROM date INNER JOIN turn ON (date.id = turn.date) GROUP BY date.id, date.date, date.type
