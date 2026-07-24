import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import { describe, it, expect } from 'vitest';
import MascotasAsociadasTable from './MascotasAsociadasTable';

const mascotas = [
  { id_mascota: 1, nombre: 'Max', especie: 'Perro' },
  { id_mascota: 2, nombre: 'Luna', especie: 'Gato' },
];

describe('MascotasAsociadasTable', () => {
  it('muestra el nombre y la especie de cada mascota', () => {
    render(
      <MemoryRouter>
        <MascotasAsociadasTable mascotas={mascotas} />
      </MemoryRouter>
    );

    expect(screen.getByText('Max')).toBeInTheDocument();
    expect(screen.getByText('Perro')).toBeInTheDocument();
    expect(screen.getByText('Luna')).toBeInTheDocument();
    expect(screen.getByText('Gato')).toBeInTheDocument();
  });

  it('cada nombre enlaza a la ficha de esa mascota', () => {
    render(
      <MemoryRouter>
        <MascotasAsociadasTable mascotas={mascotas} />
      </MemoryRouter>
    );

    expect(screen.getByRole('link', { name: 'Max' })).toHaveAttribute(
      'href',
      '/mascotas/1'
    );
    expect(screen.getByRole('link', { name: 'Luna' })).toHaveAttribute(
      'href',
      '/mascotas/2'
    );
  });
});