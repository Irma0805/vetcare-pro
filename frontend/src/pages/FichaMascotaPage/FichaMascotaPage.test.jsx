import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import FichaMascotaPage from './FichaMascotaPage';
import { obtenerFichaMascota } from '../../api/mascotas';

vi.mock('../../api/mascotas', () => ({
  obtenerFichaMascota: vi.fn(),
}));

const fichaMock = {
  id_mascota: 1,
  nombre: 'Toby',
  especie: 'Perro',
  raza: 'Labrador',
  fecha_nacimiento: '2020-05-12',
  peso: 12.5,
  activo: true,
  propietario: { id_propietario: 5, nombre: 'María', apellidos: 'López García' },
};

function renderConRuta() {
  return render(
    <MemoryRouter initialEntries={['/mascotas/1']}>
      <Routes>
        <Route path="/mascotas/:id" element={<FichaMascotaPage />} />
      </Routes>
    </MemoryRouter>
  );
}

describe('FichaMascotaPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('muestra el spinner mientras carga', () => {
    obtenerFichaMascota.mockReturnValue(new Promise(() => {}));
    renderConRuta();

    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('muestra la ficha completa cuando la carga tiene éxito', async () => {
    obtenerFichaMascota.mockResolvedValue(fichaMock);
    renderConRuta();

    await waitFor(() => {
      expect(screen.getByText('Toby')).toBeInTheDocument();
    });
    expect(screen.getByText('María López García')).toBeInTheDocument();
    expect(obtenerFichaMascota).toHaveBeenCalledWith('1');
  });

  it('muestra un mensaje de error si la mascota no existe', async () => {
    obtenerFichaMascota.mockRejectedValue({
      response: { data: { detail: 'La mascota indicada no existe' } },
    });
    renderConRuta();

    await waitFor(() => {
      expect(
        screen.getByText('La mascota indicada no existe')
      ).toBeInTheDocument();
    });
  });
});