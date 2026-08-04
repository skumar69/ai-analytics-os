import { Grid, Skeleton, Card, CardContent } from "@mui/material";

export function KPISkeletons({ count = 4 }) {
  return (
    <Grid container spacing={3}>
      {Array.from({ length: count }).map((_, i) => (
        <Grid item xs={12} sm={6} md={3} key={i}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Skeleton variant="text" width="60%" />
              <Skeleton variant="text" width="40%" height={50} />
              <Skeleton variant="text" width="80%" />
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}

export function ChartSkeleton({ height = 280 }) {
  return (
    <Card sx={{ borderRadius: 3 }}>
      <CardContent>
        <Skeleton variant="text" width="40%" height={28} sx={{ mb: 1 }} />
        <Skeleton variant="rectangular" height={height} sx={{ borderRadius: 2 }} />
      </CardContent>
    </Card>
  );
}

export function TableSkeleton({ rows = 5 }) {
  return (
    <Card sx={{ borderRadius: 3 }}>
      <CardContent>
        <Skeleton variant="text" width="35%" height={28} sx={{ mb: 2 }} />
        {Array.from({ length: rows }).map((_, i) => (
          <Skeleton key={i} variant="text" height={36} sx={{ mb: 0.5 }} />
        ))}
      </CardContent>
    </Card>
  );
}
