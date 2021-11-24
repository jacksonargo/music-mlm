import { Container, TextField } from "@mui/material";
import { useState } from "react";

function App() {
  const [context, setContext] = useState("");
  const [cursorAt, setCursorAt] = useState(0);

  const clean = context
    .replaceAll(/(\w)-\s*[\n\r]/g, "$1")
    .replaceAll(/\s+/g, " ");

  return (
    <Container>
      <TextField
        multiline
        fullWidth
        label={"Context"}
        onChange={(e) => {
          setContext(e.currentTarget.value);
        }}
      />
      <h3>Context</h3>
      <p>
        {}
        {Array.from(clean).map((d, i) => (
          <span key={i} onClick={() => setCursorAt(i)}>
            <span
              style={{
                textDecoration: cursorAt === i ? "underline" : undefined,
              }}
            >
              {d}
            </span>
          </span>
        ))}
      </p>
      <h3>Cursor At</h3>
      {cursorAt}
    </Container>
  );
}

export default App;
