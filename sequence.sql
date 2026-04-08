SELECT setval(
  pg_get_serial_sequence('"credenciales_credencialprograma"', 'creprocod'),
  (SELECT MAX("creprocod") FROM "credenciales_credencialprograma")
);