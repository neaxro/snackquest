import { Outlet, NavLink } from "react-router-dom";
import { Container, Navbar, Nav } from "react-bootstrap";

function MainLayout() {
  return (
    <div className="layout-wrapper">
      {/* Navbar */}
      <Navbar expand="lg">
        <Container>
          <Navbar.Brand as={NavLink} to="/">
            Snackquest
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="nav" />
          <Navbar.Collapse id="nav">
            <Nav className="me-auto">
              <Nav.Link as={NavLink} to="/" end>
                Home
              </Nav.Link>
              <Nav.Link as={NavLink} to="/calculator">
                Calculator
              </Nav.Link>
              <Nav.Link as={NavLink} to="/machines">
                Machines
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Page Content */}
      <div className="layout-content">
        <Container className="mt-4">
          <Outlet />
        </Container>
      </div>

      {/* Footer */}
      <footer className="container">
        <div className="d-flex flex-wrap justify-content-center align-items-center py-3 my-4 border-top">
          Made with ❤️ by the Snackquest team. Questions?{" "}
          <a href="https://github.com/neaxro/snackquest" className="ms-1">
            Contact Us
          </a>
          .
        </div>
      </footer>
    </div>
  );
}

export default MainLayout;
