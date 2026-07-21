import { Outlet, NavLink } from 'react-router'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Container from 'react-bootstrap/Container'
import PawIcon from '../../assets/icons/paw.svg?react'

function PageLayout() {
  return (
    <>
      <Navbar bg="primary" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand as={NavLink} to="/dashboard">
            <PawIcon className="me-2" width="24" height="24" />
            VetCare Pro
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="main-nav" />
          <Navbar.Collapse id="main-nav">
            <Nav>
              <Nav.Link as={NavLink} to="/veterinarios">
                Veterinarios
              </Nav.Link>
              <Nav.Link as={NavLink} to="/citas">
                Citas
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Container className="mt-4">
        <Outlet />
      </Container>
    </>
  )
}

export default PageLayout