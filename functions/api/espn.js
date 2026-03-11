export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const path = url.searchParams.get("path");

  if (!path) {
    return new Response(
      JSON.stringify({
        ok: false,
        error: "Falta el parámetro 'path'"
      }),
      {
        status: 400,
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        }
      }
    );
  }

  const espnUrl = `https://site.api.espn.com${path}`;

  try {
    const response = await fetch(espnUrl, {
      headers: {
        "User-Agent": "Mozilla/5.0"
      }
    });

    if (!response.ok) {
      return new Response(
        JSON.stringify({
          ok: false,
          error: `ESPN respondió con ${response.status}`,
          url: espnUrl
        }),
        {
          status: 502,
          headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Cache-Control": "no-store"
          }
        }
      );
    }

    const data = await response.text();

    return new Response(data, {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "public, max-age=60"
      }
    });
  } catch (error) {
    return new Response(
      JSON.stringify({
        ok: false,
        error: "No se pudo conectar con ESPN",
        detail: String(error),
        url: espnUrl
      }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "no-store"
        }
      }
    );
  }
}