import { useState } from 'react';
import { useNavigate } from 'react-router';
import { Container, Card, Alert, Form, Button } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext.jsx';
import PawIcon from '../../assets/icons/paw.svg?react';
import styles from './LoginPage.module.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [validated, setValidated] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    const form = event.currentTarget;
    event.preventDefault();

    if (form.checkValidity() === false) {
      event.stopPropagation();
      setValidated(true);
      return;
    }

    setErrorMessage('');
    setLoading(true);
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail || 'No se pudo iniciar sesión. Inténtalo de nuevo.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center min-vh-100">
      <div className={styles.loginWrapper}>
        <div className="text-center mb-4">
          <PawIcon className={`text-primary ${styles.logo}`} />
          <h1 className="text-primary fw-bold">VetCare Pro</h1>
          <p className="text-secondary text-uppercase small">Gestión Veterinaria Profesional</p>
        </div>

        <Card>
          <Card.Header as="h2" className="h5">Iniciar sesión</Card.Header>
          <Card.Body>
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

            <Form noValidate validated={validated} onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="username">
                <Form.Label>Usuario</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Ingrese su usuario"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  El usuario es obligatorio.
                </Form.Control.Feedback>
              </Form.Group>

              <Form.Group className="mb-3" controlId="password">
                <Form.Label>Contraseña</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  La contraseña es obligatoria.
                </Form.Control.Feedback>
              </Form.Group>

              <Button variant="primary" type="submit" className="w-100" disabled={loading}>
                {loading ? 'Iniciando sesión...' : 'Iniciar sesión'}
              </Button>
            </Form>
          </Card.Body>
        </Card>
      </div>
    </Container>
  );
}

export default LoginPage;