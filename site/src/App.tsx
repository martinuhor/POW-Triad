import { Artifacts } from "./components/Artifacts";
import { ChapterDataWall } from "./components/ChapterDataWall";
import { ChapterMacro } from "./components/ChapterMacro";
import { Footer } from "./components/Footer";
import { Hero } from "./components/Hero";
import { Nav } from "./components/Nav";
import { Synthesis } from "./components/Synthesis";
import { Thesis } from "./components/Thesis";

export default function App() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Thesis />
        <ChapterDataWall />
        <ChapterMacro />
        <Synthesis />
        <Artifacts />
      </main>
      <Footer />
    </>
  );
}
