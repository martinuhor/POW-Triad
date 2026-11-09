import katex from "katex";
import "katex/dist/katex.min.css";

type Props = {
  tex: string;
  display?: boolean;
  className?: string;
};

export function Formula({ tex, display = false, className }: Props) {
  const html = katex.renderToString(tex, {
    throwOnError: false,
    displayMode: display,
  });
  return (
    <span
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
