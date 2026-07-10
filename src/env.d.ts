/// <reference types="astro/client" />

// O pacote @fontsource-variable é só CSS: não traz declarações de tipo, e o
// `astro check` reclama do import de efeito colateral em src/layouts/Base.astro.
declare module '@fontsource-variable/montserrat';
