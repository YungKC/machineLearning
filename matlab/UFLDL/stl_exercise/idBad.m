index = 0;
toView = zeros(784,40);
for n=1:15298
	if pred(n) ~= testLabels(n)
		index = index+1;
		disp(sprintf('%d %d %d %d', index, n, pred(n)-1, testLabels(n)-1));
		toView(:,index) = testData(:,n);
		if index >= 40
			break;
		end
	end
end
display_network(toView);