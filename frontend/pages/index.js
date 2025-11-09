import dynamic from "next/dynamic";

const TestPanel = dynamic(() => import("../components/TestPanel"), {
  ssr: false,
});

export default function Home() {
  return (
    <div>
      <h1>Wildberries Card Generator</h1>
      <TestPanel />
    </div>
  );
}
