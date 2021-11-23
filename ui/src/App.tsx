import { Container, TextField } from "@mui/material";
import { useState } from "react";

function App() {
  const [context, setContext] = useState("");
  const [cursorAt, setCursorAt] = useState(0);

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
        {Array.from(
          context
            .split(" ")
            .filter((d) => d.length > 0)
            .join(" ")
        ).map((d, i) => (
          <span key={i} onClick={() => setCursorAt(i)}>
            {cursorAt === i ? (
              <span style={{ textDecoration: "underline" }}>{d}</span>
            ) : (
              d
            )}
          </span>
        ))}
      </p>
      <h3>Cursor At</h3>
      {cursorAt}
    </Container>
  );
}

export default App;
