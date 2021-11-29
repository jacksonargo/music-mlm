import {
  Box,
  Container,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
} from "@mui/material";
import { useEffect, useState } from "react";

const MASK_TOKEN = "[MASK]";
const PAD_TOKEN = "[PAD]";

interface UnmaskApiResponse {
  result: UnmaskResult[];
}

interface UnmaskResult {
  score: number;
  sequence: string;
  token: number;
  token_str: string;
}

function App() {
  return (
    <Container>
      <Stack spacing={4}>
        <h1>Music Production Masked Language Model</h1>
        <NextWordPrediction />
        <FillInTheBlank />
      </Stack>
    </Container>
  );
}

function NextWordPrediction() {
  const formatInput = (input: string) => `${input} ${MASK_TOKEN} ${PAD_TOKEN}`;
  const defaultSentence = "Is mayonnaise an";
  const [sentence, setSentence] = useState(formatInput(defaultSentence));
  const results = useUnmaskResults(sentence);
  return (
    <Stack spacing={2}>
      <Box>
        <h2>Next Word Prediction</h2>
        <em>Let the model predict the next word in the sentence.</em>
      </Box>
      <Box>
        <TextField
          fullWidth
          label={"Sentence"}
          defaultValue={defaultSentence}
          onChange={(e) => setSentence(formatInput(e.currentTarget.value))}
        />
      </Box>
      <Box>
        <h3>Input</h3>
        {sentence}
        <h3>Results</h3>
        {resultsTable(results)}
      </Box>
    </Stack>
  );
}

function FillInTheBlank() {
  const defaultSentence = "Mayonnaise is a [MASK].";
  const [sentence, setSentence] = useState(defaultSentence);
  const results = useUnmaskResults(sentence);
  const MASK = <span style={{ font: "monospace" }}>[MASK]</span>;
  return (
    <Stack spacing={2}>
      <Box>
        <h2>Fill in the {MASK}</h2>
        <em>Let the model predict the masked word.</em>
        <ul>
          <li>You have to include {MASK} in the sentence.</li>
          <li>You can only have on {MASK} in the sentence.</li>
          <li>Use complete sentences with punctuation.</li>
        </ul>
      </Box>
      <Box>
        <TextField
          fullWidth
          label={"Sentence"}
          defaultValue={defaultSentence}
          onChange={(e) => setSentence(e.currentTarget.value)}
        />
      </Box>
      <Box>
        <h3>Input</h3>
        {sentence}
        <h3>Results</h3>
        {resultsTable(results)}
      </Box>
    </Stack>
  );
}

function resultsTable(results: UnmaskResult[] | undefined) {
  return (
    <Table size={"small"}>
      <TableHead>
        <TableRow>
          <TableCell>Sequence</TableCell>
          <TableCell>Score</TableCell>
          <TableCell>Token ID</TableCell>
          <TableCell>Token String</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {results?.map((r, i) => (
          <TableRow key={i}>
            <TableCell>
              {r.sequence.charAt(0).toUpperCase() + r.sequence.slice(1)}
            </TableCell>
            <TableCell>{r.score}</TableCell>
            <TableCell style={{ font: "monospace" }}>{r.token}</TableCell>
            <TableCell style={{ font: "monospace" }}>{r.token_str}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

export default App;

function useUnmaskResults(sentence: string): UnmaskResult[] | undefined {
  const [results, setResults] = useState<UnmaskApiResponse | undefined>(
    undefined
  );
  useEffect(() => {
    if (!sentence.includes(MASK_TOKEN)) return;
    unmask(sentence).then((newResults) => setResults(newResults));
  }, [sentence]);
  return results?.result;
}

function unmask(sentence: string): Promise<UnmaskApiResponse> {
  return fetch("/api/unmask", {
    method: "POST",
    body: JSON.stringify({ sentence }),
  })
    .then((resp) => resp.json())
    .then((data) => data as UnmaskApiResponse);
}
