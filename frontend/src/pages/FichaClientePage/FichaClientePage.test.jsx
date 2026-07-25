import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import FichaClientePage from './FichaClientePage';
import { obtenerFichaCliente } from '../../api/propietarios';

vi.mock('../../api/propietarios', () => ({
  obtenerFichaCliente: vi.fn(),
}));

const fichaMock = {
  id_propietario: 5,
  nombre: 'Carlos Javier',
  apellidos: 'Méndez Rodríguez',
  dni: '12345678Z',
  telefono: '+34 612 345 678',
  email: 'c.mendez@example.com',
  direccion: 'Calle de la Victoria, 42',
  mascotas: [{ id_mascota: 1, nombre: 'Max', especie: 'Perro' }],
};

function renderConRuta() {
  return render(
    <MemoryRouter initialEntries={['/clientes/5']}>
      <Routes>
        <Route path="/clientes/:id" element={<FichaClientePage />} />
      </Routes>
    </MemoryRouter>
  );
}

describe('FichaClientePage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('muestra el spinner mientras carga', () => {
    obtenerFichaCliente.mockReturnValue(new Promise(() => {}));
    renderConRuta();

    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('muestra la ficha completa cuando la carga tiene éxito', async () => {
    obtenerFichaCliente.mockResolvedValue(fichaMock);
    renderConRuta();

    await waitFor(() => {
      expect(screen.getByText('Carlos Javier')).toBeInTheDocument();
    });
    expect(screen.getByText('Max')).toBeInTheDocument();
    expect(obtenerFichaCliente).toHaveBeenCalledWith('5');
  });

  it('muestra un mensaje de error si el cliente no existe', async () => {
    obtenerFichaCliente.mockRejectedValue({
      response: { data: { detail: 'El cliente indicado no existe' } },
    });
    renderConRuta();

    await waitFor(() => {
      expect(
        screen.getByText('El cliente indicado no existe')
      ).toBeInTheDocument();
    });
  });
});