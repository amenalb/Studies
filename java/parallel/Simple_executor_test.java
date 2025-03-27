import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.*;
import java.util.Scanner;

public class Simple_executor_test {

//	private static final int NTHREADS = 10;
	private static final int TASKS = 50;

	public static void main(String[] args) {
	    
        Scanner scanner = new Scanner(System.in);
		System.out.print("Podaj dokladnosc calkowania (dx): ");
		double dx = scanner.nextDouble();
		System.out.print("Podaj ilosc watkow ");
		int NTHREADS = scanner.nextInt();

		double xp = 0;
		double xk = Math.PI;
	//	double dx=0.001;

		ExecutorService executor = Executors.newFixedThreadPool(NTHREADS);
		double step = (xk - xp) / TASKS;
		List<Future<Double>> wyniki = new ArrayList<>();

for (int i = 0; i < TASKS; i++) {
			double xp_local = xp + i * step;
			double xk_local = xp_local + step;

			// Tworzymy zadanie i dodajemy do puli
			Calka_callable zadanie = new Calka_callable(xp_local, xk_local, dx);
			wyniki.add(executor.submit(zadanie));
		}
		
		double wynikRownolegly = 0;
		for (Future<Double> future : wyniki) {
			try {
				double czesciowy = future.get();
//				System.out.printf("Częściowy wynik z zadania: "+ czesciowy+"\n");
				wynikRownolegly += czesciowy;
			} catch (InterruptedException | ExecutionException e) {
				e.printStackTrace();
			}
		}

		executor.shutdown();

		// Wait until all threads finish
		while (!executor.isTerminated()) {}

		System.out.println("Finished all threads");
			System.out.println("Wynik równoległy"+ wynikRownolegly);
	}
}
