INSERT INTO `users` (`nim`, `email`, `password`, `user_role`) VALUES
(2400000, 'johnd@gmail.com', '$2b$12$mB8kymUHuLwU0S5aLuUdsORwM0dJhKFVr3rsAzhGSmxmjCq4KIL2W', 'mahasiswa'),
(2400790, 'tes@gmail.com', '$2b$12$m7FTJcv5De6DnjOVYLym/uoBA6DnzkXz8DQ04dLkY8rl2aW8GwcVC', 'admin'),
(2400987, 'tes2@gmail.com', '$2b$12$jcfir8SzEkHiEC3YZPa8YOQo/D6OpU/xWqhB2dldm7PcAOoptQZJy', 'mahasiswa');

INSERT INTO `kelas` (`kode_kelas`, `informasi_kelas`) VALUES
('20.4A.03.011', 'Lab. Inovasi Teknologi dan Media Digital, Kantor Administrasi UPI Cibiru Lt. 3 Ruang 011'),
('20.4B.02.006', 'Gedung Baru Lt. 2 Ruang 006'),
('20.4B.02.007', 'Gedung Baru Lt. 2 Ruang 007'),
('20.4B.04.006', 'Gedung Baru Lt. 4 Ruang 006'),
('20.4B.05.000', 'Gedung Baru Lt. 5 Ruang 000'),
('20.4E.02.006', 'Lab.Kom RPL Gedung Perkuliahan Baru Cibiru Lt. 2 Ruang 006'),
('20.4E.03.001', 'Gedung Perkuliahan Baru Cibiru Lt. 3 Ruang 001');

INSERT INTO `mata_kuliah` (`kode_matkul`, `nama_matkul`) VALUES
('KU100', 'Pendidikan Agama Islam'),
('KU106', 'Pendidikan Bahasa Indonesia'),
('KU110', 'Pendidikan Pancasila'),
('RL115', 'Literasi Teknologi Informasi dan Komunikasi'),
('RL116', 'Pengantar Rekayasa Perangkat Lunak'),
('RL117', 'Dasar Pemrograman'),
('RL118', 'Matematika Dasar');

INSERT INTO `dosen` (`nip`, `nama`, `alamat`, `email`, `no_tlp`) VALUES
(10001, 'Dr. Jaenuri,S.Ag,M.Pd.', 'Cibiru 1', 'jaenuri@upi.edu', '082465387612'),
(10002, 'Fully Rakhmayanti, M.Pd.', 'Cibiru 2', 'fully@upi.edu', '081245758912'),
(10003, 'Yayang Furi Furnamasari, M.Pd.', 'Cibiru 3', 'yayang@upi.edu', '082165758921'),
(10004, 'Yulia Retnowati, S.Pd.,M.T.', 'Cibiru 4', 'yulia@upi.edu', '087827456871'),
(10005, 'Dian Anggraini, S.ST.,M.T.', 'Cibiru 5', 'dian@upi.edu', '082761568761'),
(10006, 'Indira Syawanodya, S.Kom., M.Kom.', 'Cibiru 6', 'indira@upi.edu', '087812574562'),
(10007, 'Fahmi Candra Permana, S.Si., M.T.', 'Cibiru 7', 'fahmi@upi.edu', '083287614981'),
(10008, 'Asep Rudi Nurjaman, M.Pd.', 'Cibiru 8', 'asep@upi.edu', '089876895264'),
(10009, 'Raditya Muhammad, S.T.,MT.', 'Cibiru 9', 'raditya@upi.edu', '081276856524');

INSERT INTO `jadwal_dosen` (`id`, `nip`, `hari`, `jam_mulai`, `jam_selesai`) VALUES
(6, 10001, 'Senin', '07:00:00', '12:00:00'),
(7, 10001, 'Selasa', '09:00:00', '14:00:00'),
(8, 10001, 'Rabu', '13:00:00', '15:00:00'),
(9, 10001, 'Kamis', '15:00:00', '17:00:00'),
(10, 10001, 'Jumat', '09:00:00', '12:00:00'),
(11, 10001, 'Sabtu', '15:00:00', '17:00:00'),
(12, 10002, 'Senin', '09:00:00', '12:00:00'),
(13, 10002, 'Selasa', '10:00:00', '17:00:00'),
(14, 10002, 'Rabu', '15:00:00', '18:00:00'),
(15, 10002, 'Kamis', '07:00:00', '12:00:00'),
(16, 10002, 'Jumat', '08:00:00', '11:00:00'),
(17, 10003, 'Senin', '07:30:00', '15:00:00'),
(18, 10003, 'Selasa', '15:00:00', '19:00:00'),
(19, 10003, 'Rabu', '14:00:00', '17:00:00'),
(20, 10003, 'Kamis', '09:00:00', '12:00:00'),
(21, 10003, 'Jumat', '13:00:00', '15:00:00'),
(22, 10004, 'Senin', '08:00:00', '12:00:00'),
(23, 10004, 'Selasa', '07:00:00', '10:00:00'),
(24, 10004, 'Rabu', '15:00:00', '18:00:00'),
(25, 10004, 'Kamis', '10:00:00', '15:00:00'),
(26, 10004, 'Jumat', '12:00:00', '15:00:00'),
(27, 10005, 'Senin', '07:00:00', '12:00:00'),
(28, 10005, 'Selasa', '09:00:00', '14:00:00'),
(29, 10005, 'Rabu', '13:00:00', '17:00:00'),
(30, 10005, 'Kamis', '08:00:00', '13:00:00'),
(31, 10005, 'Jumat', '09:00:00', '18:00:00'),
(32, 10006, 'Senin', '07:00:00', '15:00:00'),
(33, 10006, 'Selasa', '09:00:00', '12:00:00'),
(34, 10006, 'Rabu', '13:00:00', '16:00:00'),
(35, 10006, 'Kamis', '10:00:00', '15:00:00'),
(36, 10006, 'Jumat', '07:00:00', '11:00:00'),
(37, 10007, 'Senin', '08:00:00', '11:00:00'),
(38, 10007, 'Selasa', '09:00:00', '14:00:00'),
(39, 10007, 'Rabu', '10:00:00', '18:00:00'),
(40, 10007, 'Kamis', '11:00:00', '15:00:00'),
(41, 10007, 'Jumat', '12:00:00', '17:00:00'),
(42, 10008, 'Senin', '07:00:00', '12:00:00'),
(43, 10008, 'Selasa', '12:00:00', '15:00:00'),
(44, 10008, 'Rabu', '10:00:00', '16:00:00'),
(45, 10008, 'Kamis', '08:00:00', '14:00:00'),
(46, 10008, 'Jumat', '09:00:00', '12:00:00'),
(47, 10009, 'Senin', '07:00:00', '11:00:00'),
(48, 10009, 'Selasa', '10:00:00', '15:00:00'),
(49, 10009, 'Rabu', '07:00:00', '14:00:00'),
(50, 10009, 'Kamis', '08:00:00', '14:00:00'),
(51, 10009, 'Jumat', '09:00:00', '17:00:00'),
(52, 10008, 'Rabu', '08:00:00', '12:00:00'),
(53, 10002, 'Jumat', '10:00:00', '13:00:00'),
(54, 10003, 'Rabu', '13:00:00', '14:40:00');

INSERT INTO `detail_kelas` (`id_detail_kelas`, `kode_kelas`, `kode_matkul`, `hari`, `jam_mulai`, `jam_selesai`, `nip_dosen`, `informasi_kelas`, `pengguna`, `status`) VALUES
(17, '20.4B.02.007', 'KU100', 'Rabu', '08:40:00', '10:20:00', 10008, 'Gedung Baru Lt. 2 Ruang 007', 'RPL 1-A', 'Digunakan'),
(18, '20.4B.05.000', 'KU106', 'Jumat', '10:20:00', '12:00:00', 10002, 'Gedung Baru Lt. 5 Ruang 000', 'RPL 1-A', 'Digunakan'),
(19, '20.4B.02.007', 'KU110', 'Rabu', '13:00:00', '14:40:00', 10003, 'Gedung Baru Lt. 2 Ruang 007', 'RPL 1-A', 'Digunakan'),
(20, '20.4E.02.006', 'RL115', 'Selasa', '13:00:00', '15:00:00', 10004, 'Gedung Baru Lt. 2 Ruang 006', 'RPL 1-A', 'Digunakan'),
(21, '20.4E.02.006', 'RL116', 'Senin', '13:00:00', '15:30:00', 10005, 'Gedung Baru Lt. 2 Ruang 006', 'RPL 1-A', 'Digunakan'),
(22, '20.4E.02.006', 'RL117', 'Selasa', '08:40:00', '12:00:00', 10006, 'Gedung Baru Lt. 2 Ruang 006', 'RPL 1-A', 'Digunakan'),
(24, '20.4B.04.006', 'RL118', 'Senin', '07:00:00', '10:20:00', 10009, 'Gedung Baru Lt. 4 Ruang 006', 'RPL 1-A', 'Digunakan'),
(27, '20.4B.02.007', 'KU100', 'Senin', '07:00:00', '09:20:00', 10008, 'Gedung Baru Lt. 2 Ruang 007', 'RPL 1-C', 'Digunakan'),
(28, '20.4A.03.011', 'KU110', 'Senin', '08:40:00', '12:00:00', 10003, 'Lab. Inovasi Teknologi dan Media Digital, Kantor Administrasi UPI Cibiru Lt. 3 Ruang 011', 'RPL 1-C', 'Digunakan'),
(29, '20.4A.03.011', 'KU110', 'Selasa', '07:00:00', '09:20:00', 10003, 'Lab. Inovasi Teknologi dan Media Digital, Kantor Administrasi UPI Cibiru Lt. 3 Ruang 011', '', 'Tersedia'),
(30, '20.4A.03.011', 'RL118', 'Jumat', '07:00:00', '10:20:00', 10007, '', '', 'Tersedia'),
(31, '20.4A.03.011', 'RL115', 'Rabu', '15:00:00', '17:00:00', 10004, '', '', 'Tersedia'),
(32, '20.4A.03.011', 'RL115', 'Kamis', '10:00:00', '13:00:00', 10004, '', '', 'Tersedia'),
(33, '20.4A.03.011', 'RL118', 'Jumat', '07:00:00', '10:20:00', 10009, 'Lab. Inovasi Teknologi dan Media Digital, Kantor Administrasi UPI Cibiru Lt. 3 Ruang 011', 'RPL 1-C', 'Digunakan'),
(39, '20.4E.03.001', 'KU100', 'Senin', '07:00:00', '10:00:00', 10001, 'RPL 1-C [ 2 SKS ]Gedung Perkuliahan Baru Cibiru Lt. 3 Ruang 001', '', 'Tersedia'),
(40, '20.4E.03.001', 'KU100', 'Selasa', '09:00:00', '12:00:00', 10001, 'RPL 1-C [ 2 SKS ]Gedung Perkuliahan Baru Cibiru Lt. 3 Ruang 001', 'RPL 1-C', 'Digunakan'),
(41, '20.4E.03.001', 'KU100', 'Rabu', '13:00:00', '14:40:00', 10001, 'RPL 1-C [ 2 SKS ]Gedung Perkuliahan Baru Cibiru Lt. 3 Ruang 001', '', 'Tersedia');

INSERT INTO `transaksi` (`id_transaksi`, `id_detail_kelas`, `nim`, `email`, `tanggal_transaksi`, `status_transaksi`, `pengguna`, `komentar`) VALUES
(9, 29, 2400987, 'tes2@gmail.com', '2024-12-25 10:35:28', 'Pengajuan Dibatalkan', 'RPL 1-C', NULL),
(10, 29, 2400987, 'tes2@gmail.com', '2024-12-25 10:36:04', 'ACC Pembatalan', 'RPL 1-C', NULL);

INSERT INTO `pengajuan` (`id_pengajuan`, `id_detail_kelas`, `nim`, `email`, `kode_kelas`, `kode_matkul`, `hari`, `jam_mulai`, `jam_selesai`, `nip_dosen`, `nama_dosen`, `informasi_kelas`, `pengguna`, `tgl_pengajuan`, `status_pengajuan`, `komentar`) VALUES
(8, 39, 2400987, 'tes2@gmail.com', '20.4E.03.001', 'KU100', 'Senin', '07:00:00', '10:00:00', 10001, 'Dr. Jaenuri,S.Ag,M.Pd.', 'RPL 1-C [ 2 SKS ]Gedung Perkuliahan Baru Cibiru Lt. 3 Ruang 001', 'RPL 1-C', '2024-12-29 15:44:29', 'ACC Pembatalan', 'acc'),
(9, 40, 2400987, 'tes2@gmail.com', '20.4E.03.001', 'KU100', 'Selasa', '09:00:00', '12:00:00', 10001, 'Dr. Jaenuri,S.Ag,M.Pd.', 'RPL 1-C [ 2 SKS ]Gedung Perkuliahan Baru Cibiru Lt. 3 Ruang 001', 'RPL 1-C', '2024-12-29 15:57:09', 'ACC Pengajuan', ''),
(10, 41, 2400987, 'tes2@gmail.com', '20.4E.03.001', 'KU100', 'Rabu', '13:00:00', '14:40:00', 10001, 'Dr. Jaenuri,S.Ag,M.Pd.', 'RPL 1-C [ 2 SKS ]Gedung Perkuliahan Baru Cibiru Lt. 3 Ruang 001', 'RPL 1-C', '2024-12-29 16:00:59', 'ACC Pembatalan', 'acc');